import os
import pickle  # Use pickle instead of JSON
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    """Authenticate with Google Drive, handling expired tokens and missing credentials."""
    creds = None
    token_file = 'token.pickle'
    credentials_file = Path("credentials.json")

    # Load token.pickle if it exists
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or request new authentication if necessary
    if not creds or not creds.valid:
        try:
            # Attempt to refresh the token if it is expired and has a refresh token
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception("No valid or refreshable token available.")
        except Exception as e:
            # Fallback to new authentication flow
            print(f"[INFO] Authentication required: {e}")
            if credentials_file.exists():  # Fallback to credentials.json
                flow = InstalledAppFlow.from_client_secrets_file(str(credentials_file), SCOPES)
            else:
                raise FileNotFoundError(
                    "No valid credentials found. Ensure `credentials.json` exists."
                )

            creds = flow.run_local_server(port=0)

        # Save credentials to token.pickle for reuse
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)
