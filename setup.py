import json
import os
import subprocess
import shutil
from pathlib import Path


def get_venv_python():
    """Get the Python interpreter path from the virtual environment."""
    return os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")

def detect_python_command():
    """Detect the working Python command on the user's device."""
    possible_commands = [
        "python", "python3", "python3.11", "python3.10", "python3.9", "python3.8", 
        "py"  # Common on Windows
    ]
    for command in possible_commands:
        try:
            result = subprocess.run([command, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Detected Python command: {command} ({result.stdout.strip()})")
                return command
        except FileNotFoundError:
            continue

    fallback = input("No Python command detected. Please provide your Python command (e.g., python3.9): ").strip()
    try:
        result = subprocess.run([fallback, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Using provided Python command: {fallback} ({result.stdout.strip()})")
            return fallback
    except FileNotFoundError:
        pass

    raise EnvironmentError("No suitable Python interpreter found. Please install Python and try again.")


def create_virtual_environment():
    """Create a virtual environment using the detected Python command."""
    print("Creating a virtual environment...")
    python_command = detect_python_command()
    try:
        subprocess.run([python_command, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the virtual environment: {e}")


def install_requirements_in_venv():
    """Install required Python packages in the virtual environment."""
    venv_python = get_venv_python()
    print("Installing required Python packages in the virtual environment...")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)  # Upgrade pip
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing requirements: {e}")


def build_executable():
    """Build an executable using PyInstaller in the virtual environment."""
    print("Building the executable with PyInstaller...")
    venv_python = get_venv_python()
    try:
        subprocess.run(
            [
                venv_python,
                "-m",
                "PyInstaller",
                "--onefile",
                "--name=sdrive",
                "sdrive/main.py",
            ],
            check=True,
        )
        print("Executable built successfully! Check the `dist` folder.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while building the executable: {e}")


def clean_up():
    """Clean up unnecessary files and folders after building."""
    print("Cleaning up...")
    paths_to_remove = ["__pycache__", "build", "main.spec", "venv", "credentials.py"]
    for path in paths_to_remove:
        path_obj = Path(path)
        if path_obj.exists():
            if path_obj.is_dir():
                shutil.rmtree(path)
            else:
                path_obj.unlink()
            print(f"Removed: {path}")
    print("Clean-up complete! The project is now nice and tidy.")


def main():
    print("Starting setup...")
    create_virtual_environment()
    install_requirements_in_venv()
    build_executable()
    print("Setup complete! You're ready to go!")

    # Prompt to clean up
    choice = input("\nDo you want to clean up unnecessary files? (yes/no): ").strip().lower()
    if choice in ["yes", "y"]:
        clean_up()


if __name__ == "__main__":
    main()
