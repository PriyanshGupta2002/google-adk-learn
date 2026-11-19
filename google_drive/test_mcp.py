import asyncio
import httpx2

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "https://drivemcp.googleapis.com/mcp/v1"


async def main():

    credentials = Credentials.from_authorized_user_file("token.json")

    if not credentials.valid:
        credentials.refresh(Request())

        # Persist refreshed credentials
        with open("token.json", "w") as f:
            f.write(credentials.to_json())

    headers = {"Authorization": f"Bearer {credentials.token}"}

    async with httpx2.AsyncClient(
        headers=headers,
        timeout=httpx2.Timeout(30, read=300),
    ) as http_client:

        async with streamable_http_client(
            MCP_URL,
            http_client=http_client,
        ) as (read_stream, write_stream):

            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                # Discover tools
                result = await session.list_tools()

                print("\nAvailable tools:")
                for tool in result.tools:
                    print("-", tool.name)

                # Execute actual Drive tool
                print("\nTesting Google Drive access...")

                try:
                    response = await session.call_tool(
                        "list_recent_files", arguments={}
                    )

                    print("\nComplete MCP response:")
                    print(response)

                    print("\nResponse attributes:")
                    print(response.model_dump(exclude_none=True))

                    if response.isError:
                        print("\nDrive access failed!")
                    else:
                        print("\nDrive access successful!")

                except Exception as error:
                    print("\nTool execution exception:")
                    print(repr(error))


if __name__ == "__main__":
    asyncio.run(main())
