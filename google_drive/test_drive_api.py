import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

credentials = Credentials.from_authorized_user_file("token.json")

if not credentials.valid:
    credentials.refresh(Request())

response = requests.get(
    "https://www.googleapis.com/drive/v3/files",
    headers={"Authorization": f"Bearer {credentials.token}"},
    params={"pageSize": 5, "fields": "files(id,name,mimeType)"},
)

print("Status:", response.status_code)
print("Response:", response.text)
