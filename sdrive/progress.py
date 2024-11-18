from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, DownloadColumn

def create_progress_bar():
    """Create a progress bar for file downloads."""
    return Progress(
        TextColumn("[cyan]{task.fields[file_name]}[/cyan]"),
        BarColumn(),
        DownloadColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[speed]}"),
    )
