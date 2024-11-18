# utils.py
import requests
from rich.console import Console
from sdrive.constants import FOLDER_MIME_TYPE
import re
from time import sleep
import pyfiglet

console = Console()

def extract_id(link):
    """Extract file or folder ID from a Google Drive link."""
    match = re.search(r'(?:file/d/|folders/|id=|open\?id=)([a-zA-Z0-9_-]+)', link)
    return match.group(1) if match else None

def is_folder_link(service, file_id):
    """
    Determines if a given Google Drive file ID is a folder.

    Args:
        service: The Google Drive API service instance.
        file_id (str): The file ID to check.

    Returns:
        bool: True if the file is a folder, False otherwise.
    """
    try:
        file_metadata = service.files().get(fileId=file_id, fields="mimeType").execute()
        return file_metadata["mimeType"] == FOLDER_MIME_TYPE
    except Exception as e:
        raise RuntimeError(f"Error while checking folder status: {e}")

def format_size(size):
    """
    Formats a size in bytes into a human-readable string.

    Args:
        size (int): Size in bytes.

    Returns:
        str: Human-readable size string (e.g., "2.3 MB").
    """
    if size < 1024:
        return f"{size} B"
    for unit in ["KB", "MB", "GB", "TB", "PB"]:
        size /= 1024.0
        if size < 1024:
            return f"{size:.2f} {unit}"
    return f"{size:.2f} PB"

def is_internet_connected():
    """
    Checks if the internet is connected.

    Returns:
        bool: True if the internet is connected, False otherwise.
    """
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

def wait_for_connection(interval=5):
    """Wait until the internet connection is restored."""
    while not is_internet_connected():
        console.log("[yellow]Waiting for internet connection...[/yellow]")
        sleep(interval)

def display_banner():
    """Display a fancy banner with a hidden message."""
    banner = pyfiglet.figlet_format("SDrive", font="red_phoenix")
    tiny_credit = "[dim cyan]Blackhole[/dim cyan]"
    console.print(f"[bold magenta]{banner}[/bold magenta]")
    console.print(f"\n{' ' * 10}{tiny_credit}\n")