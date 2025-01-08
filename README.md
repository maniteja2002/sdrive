![Cross-Platform Build and Upload](https://github.com/maniteja2002/sdrive/actions/workflows/build.yml/badge.svg?branch=main)



# SDrive

SDrive is a lightweight, efficient, and modular command-line tool for downloading and managing files. Designed with simplicity and functionality in mind, it provides seamless integration with external services such as Google Drive while offering advanced features like authentication, progress tracking, and concurrent downloads.

## Features

-   **User Authentication**: Secure and straightforward authentication mechanisms with 'credentials.json'.
-   **Robust Downloading**: Reliable and efficient file downloading with support for progress tracking.
-   **Modular Design**: Cleanly organized codebase, making it easy to understand, extend, and maintain.
-   **Command-Line Interface**: Intuitive CLI for managing downloads and other operations.
- **cross platform support**: you can download the executable files from the releases section for macos, windows, linux.
- **download features include**:
- RESUME SUPPORT 
- WAIT FOR INTERNET SUPPORT
- AUTO RETRY FOR DOWNLOAD SUPPORT

## Manual Installation

### Prerequisites

-   Python 3.8 or later
-   `pip` (Python package manager)
### Step1
1. visit https://console.cloud.google.com/ , and create a project.
2. open the project and go to 'APIs & Services' section and click on 'ENABLE APIS AND SERVICES'
3. Enable 'Google Drive API'.
4. create OAuth consent screen in 'APIs & Services'.
5. In credentials section click on '+ CREATE CREDENTIALS'.
6. and Click on 'OAuth Client ID', as 
- Application type --> Desktop app
7. download credentials and you will get a json file and rename it as ```credentials.json```
8. copy and paste this json file in root directory or the directory where you are running the sdrive executable.



### Step2

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/maniteja2002/sdrive.git
    cd sdrive
3.  Install SDrive using the python in the sdrive folder:
    
    ```bash
    python setup.py 
    ```
### Note: 
1. everything will installed using python virtual environment, and at the end it asks the user to remove the downloaded libraries and other dependencies. 
- If you want to delete enter 'yes' , otherwise enter 'no'.

    

## Usage

### Basic Command

-   **Download a File**:
    
    ```bash
    sdrive <file_id (or) folder_id >
    ```
    

### Examples
-   ```bash
    sdrive "https://drive.google.com/file/d/1GIrH3c3lr_MB0DpFYkiIsc-nQpQX5ULX/view?usp=drive_link" 
    ```
    

## Project Structure

```plaintext
sdrive-main/
├── .github/               # GitHub workflows and CI/CD configurations
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── setup.py               # Installation script
├── sdrive/                # Core module
│   ├── __init__.py        # Package initializer
│   ├── authentication.py  # Authentication logic
│   ├── banner.py          # CLI banner display
│   ├── cli.py             # Command-line interface logic
│   ├── constants.py       # Global constants
│   ├── downloader.py      # File downloading logic
│   ├── main.py            # Entry point
│   ├── progress.py        # Progress tracking
│   ├── utils.py           # Utility functions

```

## Development

### Setting Up

1.  Run setup file :
    ```python setup.py ```
- It will create a virtual environment inside the sdrive(root) folder and install required dependencies, but press no at the end of the setup script so that no dependencies will be deleted.
   

## Contribution Guidelines

We welcome contributions to improve SDrive! Here's how you can help:

1.  Fork the repository and create a new branch for your feature or bugfix.
2.  Write clean, modular, and well-documented code.
3.  Ensure it works before submitting your pull request.
4.  Open a pull request with a clear description of your changes.

## License

SDrive is licensed under the MIT License. You are free to use, modify, and distribute this software under the terms of the license.

## Support

For issues, questions, or feature requests, please open an issue on the [GitHub repository](https://github.com/maniteja2002/sdrive/issues).
