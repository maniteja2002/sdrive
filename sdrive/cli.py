import sys
from sdrive.utils import extract_file_id

def parse_arguments():
    """Parse command-line arguments."""
    if len(sys.argv) != 2:
        print("Usage: sdrive {Google Drive link}")
        sys.exit(1)
    return sys.argv[1].strip()

def main():
    """CLI entry point."""
    link = parse_arguments()
    file_id = extract_file_id(link)
    if not file_id:
        print("Invalid Google Drive link.")
        sys.exit(1)
    return file_id
