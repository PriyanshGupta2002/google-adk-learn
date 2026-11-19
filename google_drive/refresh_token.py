from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

token_path = Path("token.json")

credentials = Credentials.from_authorized_user_file(str(token_path))

print("Refresh token available:", bool(credentials.refresh_token))

if not credentials.refresh_token:
    raise Exception("Refresh token missing. OAuth login required again.")

credentials.refresh(Request())

# Save the updated credentials
token_path.write_text(credentials.to_json())

print("Token valid:", credentials.valid)
print("Token expired:", credentials.expired)
print("Token refreshed successfully!")
