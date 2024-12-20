import os
from time import time
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn
from sdrive.utils import wait_for_connection, format_size, calculate_folder_size
import requests

console = Console()

def download_file(service, file_id, file_name, cumulative_downloaded=0, folder_total_size=None, folder_file_count=None, current_file_index=None):
    """Download a file with progress tracking, including retry logic and download speed."""
    retry_attempts = 10
    attempt = 0

    while attempt < retry_attempts:
        try:
            # Get file size
            file_metadata = service.files().get(fileId=file_id, fields="size").execute()
            total_size = int(file_metadata["size"])
            creds = service._http.credentials
            session = requests.Session()

            # Check if file already exists and determine resume range
            existing_size = os.path.getsize(file_name) if os.path.exists(file_name) else 0
            if existing_size >= total_size:
                console.log(f"[green]{file_name} is already downloaded. Skipping.[/green]")
                cumulative_downloaded += total_size
                return cumulative_downloaded

            # Set headers for resuming
            headers = {
                "Authorization": f"Bearer {creds.token}",
                "Range": f"bytes={existing_size}-",
            }
            mode = "ab" if existing_size else "wb"

            if existing_size:
                console.log(f"[cyan]Resuming download of {file_name} from {format_size(existing_size)}.[/cyan]")
            else:
                console.log(f"[cyan]Downloading {file_name} ({format_size(total_size)})[/cyan]")

            # Start or resume download
            url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
            response = session.get(url, headers=headers, stream=True, timeout=10)  # Add timeout
            response.raise_for_status()

            start_time = time()
            downloaded_this_session = 0
            last_update_time = start_time

            with Progress(
                TextColumn(f"[cyan]({current_file_index}/{folder_file_count})[/cyan]" if folder_file_count else ""),
                BarColumn(),
                DownloadColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("{task.fields[progress_info]}"),
                TextColumn("[cyan]{task.fields[speed]}[/cyan]"),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(
                    "[cyan]Downloading file[/cyan]",
                    total=total_size,
                    completed=existing_size,
                    progress_info=f"{format_size(existing_size)}/{format_size(total_size)}",
                    speed="0.00 MB/s",
                )

                with open(file_name, mode) as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_this_session += len(chunk)
                            progress.update(task, advance=len(chunk))

                            # Update speed and progress information every second
                            current_time = time()
                            elapsed_time = current_time - last_update_time
                            if elapsed_time >= 1:
                                completed = progress.tasks[task].completed
                                speed = downloaded_this_session / elapsed_time / (1024 * 1024)  # Speed in MB/s
                                progress_info = f"{format_size(completed)}/{format_size(total_size)}"
                                progress.update(task, progress_info=progress_info, speed=f"{speed:.2f} MB/s")
                                downloaded_this_session = 0
                                last_update_time = current_time

            console.log(f"[green]Downloaded: {file_name} ({format_size(total_size)})[/green]")
            cumulative_downloaded += total_size
            return cumulative_downloaded  # Exit function after successful download

        except requests.exceptions.Timeout:
            console.log("[yellow]Connection timed out. Retrying...[/yellow]")
            attempt += 1
            wait_for_connection()

        except requests.exceptions.RequestException as e:
            attempt += 1
            console.log(f"[yellow]Request error: {e}. Retrying ({attempt}/{retry_attempts})...[/yellow]")
            wait_for_connection()

        except Exception as e:
            attempt += 1
            console.log(f"[red]Unexpected error: {e}. Retrying ({attempt}/{retry_attempts})...[/red]")
            wait_for_connection()

    console.log(f"[red]Failed to download {file_name} after {retry_attempts} attempts.[/red]")
    return cumulative_downloaded

def download_folder(service, folder_id, folder_name, cumulative_downloaded=0):
    """Download all files and subfolders from a folder recursively with folder-level progress."""
    os.makedirs(folder_name, exist_ok=True)
    query = f"'{folder_id}' in parents and trashed=false"
    page_token = None

    all_items = []

    while True:
        # Add pagination support with `pageToken`
        results = service.files().list(
            q=query,
            fields="nextPageToken, files(id, name, mimeType, size)",
            pageToken=page_token,
        ).execute()

        items = results.get("files", [])
        all_items.extend(items)

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    if not all_items:
        console.print(f"[yellow]The folder {folder_name} is empty.[/yellow]")
        return cumulative_downloaded

    # Calculate total size and file count for progress tracking
    console.log(f"[green]calculating the folder - {folder_name} size...[/green]")
    total_size = calculate_folder_size(service, folder_id)
    total_files = len(all_items)

    console.log(f"[cyan]Starting download for folder: {folder_name} ({format_size(total_size)})[/cyan]")

    for index, item in enumerate(all_items, start=1):
        item_name = item["name"]
        item_id = item["id"]
        mime_type = item["mimeType"]
        file_path = os.path.join(folder_name, item_name)

        if mime_type == "application/vnd.google-apps.folder":
            # Recursively download subfolders
            cumulative_downloaded = download_folder(service, item_id, file_path, cumulative_downloaded)
        else:
            # Download files with progress tracking and retries
            cumulative_downloaded = download_file(
                service, item_id, file_path, cumulative_downloaded, total_size, total_files, index
            )

    console.log(f"[cyan]Folder: {folder_name}[/cyan] - [green]Total downloaded: {format_size(total_size)}[/green]")
    return cumulative_downloaded