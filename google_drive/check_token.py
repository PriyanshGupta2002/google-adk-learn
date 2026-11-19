import json
from pathlib import Path
from google.oauth2.credentials import Credentials

credentials = Credentials.from_authorized_user_file("token.json")

print("Token valid:", credentials.valid)
print("Token expired:", credentials.expired)
print("Granted scopes:")

for scope in credentials.scopes or []:
    print("-", scope)

print(
    "Has Drive readonly:",
    "https://www.googleapis.com/auth/drive.readonly" in (credentials.scopes or []),
)
