from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/drive.file",
]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    scopes=SCOPES,
)

credentials = flow.run_local_server(
    port=0,
    access_type="offline",
    prompt="consent",
)

with open("token.json", "w") as token_file:
    token_file.write(credentials.to_json())

print("Google OAuth authentication successful!")
print("Access token obtained:", bool(credentials.token))
print("Refresh token obtained:", bool(credentials.refresh_token))
