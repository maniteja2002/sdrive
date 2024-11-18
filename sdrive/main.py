from sdrive.authentication import authenticate_google_drive
from sdrive.downloader import download_file, download_folder
from sdrive.utils import is_folder_link, extract_id, display_banner
from rich.console import Console

console = Console()

def main(link):
    display_banner()
    """Main entry point for downloading files or folders."""
    service = authenticate_google_drive()
    file_id = extract_id(link)
    is_folder = is_folder_link(service, file_id)

    if is_folder:
        file_metadata = service.files().get(fileId=file_id, fields="name").execute()
        folder_name = file_metadata["name"]
        download_folder(service, file_id, folder_name)
    else:
        file_metadata = service.files().get(fileId=file_id, fields="name").execute()
        file_name = file_metadata["name"]
        download_file(service, file_id, file_name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        console.print("[red]Usage:sdrive {Google Drive link}[/red]")
    else:
        main(sys.argv[1])
