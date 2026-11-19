import os
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPConnectionParams,
)

load_dotenv()

# --------------------------------
# 1. Gemini Configuration
# --------------------------------

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"


# --------------------------------
# 2. Load OAuth Credentials
# --------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / "token.json"

credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE))


def refresh_credentials():
    """Refresh and persist Google OAuth credentials."""

    if not credentials.refresh_token:
        raise RuntimeError("Refresh token missing. Please authenticate again.")

    credentials.refresh(Request())

    TOKEN_FILE.write_text(credentials.to_json())

    print("Google OAuth token refreshed successfully.")


# Refresh expired token during startup
if not credentials.valid:
    refresh_credentials()


# --------------------------------
# 3. Dynamic MCP Authentication
# --------------------------------


def auth_header_provider(context):
    """Provide a valid OAuth token for MCP requests."""

    if not credentials.valid:
        refresh_credentials()

    return {"Authorization": f"Bearer {credentials.token}"}


# --------------------------------
# 4. Google Drive MCP Connection
# --------------------------------

drive_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://drivemcp.googleapis.com/mcp/v1",
        timeout=30,
        sse_read_timeout=300,
    ),
    header_provider=auth_header_provider,
)


# --------------------------------
# 5. Google Drive Agent
# --------------------------------

root_agent = Agent(
    name="google_drive_agent",
    model="gemini-3.8-flash",
    description="AI assistant that interacts with Google Drive.",
    instruction="""
    You are a helpful Google Drive assistant.

    Your capabilities:
    - Search files in Google Drive.
    - List recent files.
    - Read document contents.
    - Retrieve file metadata.
    - Create files when explicitly requested.

    Guidelines:

    1. Always use available Drive MCP tools
       to retrieve information.

    2. Never invent file names or file contents.

    3. For counting files, retrieve the relevant
       files and calculate the count accurately.

    4. Clearly communicate if a file cannot
       be accessed due to permissions.

    5. Never claim an operation succeeded unless
       the MCP tool confirms it.
    """,
    tools=[drive_toolset],
)
