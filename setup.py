import json
import os
import subprocess
import shutil
from pathlib import Path


def get_venv_python():
    """Get the Python interpreter path from the virtual environment."""
    return os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")


def create_virtual_environment():
    """Create a virtual environment."""
    print("Creating a virtual environment...")
    python_command = input("what is your device python command eg:python or python3 :")
    subprocess.run([python_command, "-m", "venv", "venv"], check=True)
    print("Virtual environment created successfully!")


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


def read_and_generate_credentials():
    """Read `credentials.json` and create `credentials.py` with the required structure."""
    credentials_path = Path("credentials.json")
    if not credentials_path.exists():
        print("Error: `credentials.json` not found. Please provide the file and try again.")
        return

    try:
        with credentials_path.open("r") as f:
            credentials_data = json.load(f)

        # Extract required fields
        client_id = credentials_data["installed"]["client_id"]
        project_id = credentials_data["installed"]["project_id"]
        client_secret = credentials_data["installed"]["client_secret"]

        # Generate credentials.py
        credentials_py_content = f'''CLIENT_CONFIG = {{
    "installed": {{
        "client_id": "{client_id}",
        "project_id": "{project_id}",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "{client_secret}",
        "redirect_uris": [
            "http://localhost"
        ]
    }}
}}
'''
        credentials_py_path = Path("sdrive/credentials.py")
        with credentials_py_path.open("w") as f:
            f.write(credentials_py_content)

        print("Generated `credentials.py` successfully!")
    except KeyError as e:
        print(f"Error: Missing key in `credentials.json`: {e}")
    except json.JSONDecodeError:
        print("Error: Failed to parse `credentials.json`. Ensure it's a valid JSON file.")


def build_executable():
    """Build an executable using PyInstaller in the virtual environment."""
    print("Building the executable with PyInstaller...")
    venv_python = get_venv_python()

    # Find the pyfiglet fonts directory to add as data
    fonts_dir = find_pyfiglet_fonts(venv_python)
    if fonts_dir is None:
        print("Pyfiglet fonts directory could not be located. Skipping...")
        return

    try:
        subprocess.run(
            [
                venv_python,
                "-m",
                "PyInstaller",
                "--onefile",
                f"--add-data={fonts_dir}{os.pathsep}pyfiglet/fonts",
                "--name=sdrive",
                "sdrive/main.py",
            ],
            check=True,
        )
        print("Executable built successfully! Check the `dist` folder.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while building the executable: {e}")


def find_pyfiglet_fonts(venv_python):
    """Find the pyfiglet fonts folder directory."""
    try:
        result = subprocess.run(
            [venv_python, "-c", "import pyfiglet; print(pyfiglet.__file__)"],
            capture_output=True,
            text=True,
            check=True,
        )
        pyfiglet_path = Path(result.stdout.strip()).parent
        fonts_dir = pyfiglet_path / "fonts"
        if fonts_dir.exists():
            return str(fonts_dir)
        else:
            print(f"Error: Fonts directory not found in {fonts_dir}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error locating pyfiglet fonts: {e}")
        return None


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
    read_and_generate_credentials()
    build_executable()
    print("Setup complete! You're ready to go!")

    # Prompt to clean up
    choice = input("\nDo you want to clean up unnecessary files? (yes/no): ").strip().lower()
    if choice in ["yes", "y"]:
        clean_up()


if __name__ == "__main__":
    main()
