import json

with open("client_secret.json") as f:
    client_data = json.load(f)

with open("token.json") as f:
    token_data = json.load(f)

client_config = client_data.get("installed") or client_data.get("web")

configured_client_id = client_config["client_id"]
token_client_id = token_data["client_id"]

print("Same OAuth Client:", configured_client_id == token_client_id)

print("Token has refresh token:", bool(token_data.get("refresh_token")))
