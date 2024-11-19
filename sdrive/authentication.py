import os
import pickle  # Use pickle instead of JSON
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path
try:
    from sdrive.credentials import CLIENT_CONFIG  # Import CLIENT_CONFIG if available
except ImportError:
    CLIENT_CONFIG = None


SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    """Authenticate with Google Drive using sdrive.credentials or credentials.json."""
    creds = None
    token_file = 'token.pickle'
    credentials_file = Path("credentials.json")

    # Load token.pickle if it exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid creds, refresh or start a new authentication flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use CLIENT_CONFIG if sdrive.credentials exists
            if CLIENT_CONFIG:
                flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
            elif credentials_file.exists():  # Fallback to credentials.json
                flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
            else:
                raise FileNotFoundError(
                    "No valid credentials found. Ensure `sdrive.credentials` or `credentials.json` exists."
                )

            creds = flow.run_local_server(port=0)

        # Save credentials to token.pickle for reuse
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)
