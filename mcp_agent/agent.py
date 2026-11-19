import os
from pathlib import Path

from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from google.adk.tools.bash_tool import (
    ExecuteBashTool,
    BashToolPolicy,
)

from mcp import StdioServerParameters

load_dotenv()


# ----------------------------------
# 1. GitHub Configuration
# ----------------------------------

github_token = os.getenv("GITHUB_TOKEN")

if not github_token:
    raise ValueError("Add GITHUB_TOKEN to your .env file.")


# ----------------------------------
# 2. Dedicated Workspace
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent

workspace = BASE_DIR / "files" / "workspace"
workspace.mkdir(parents=True, exist_ok=True)

WORKSPACE_PATH = str(workspace.resolve())


# ----------------------------------
# 3. Shell Command Restrictions
# ----------------------------------

shell_policy = BashToolPolicy(
    allowed_command_prefixes=(
        "pwd",
        "ls ",
        "find ",
        "cat ",
        "head ",
        "tail ",
        "grep ",
        "mkdir ",
        "touch ",
        "python ",
        "uv ",
        "npm ",
        "npx ",
        "git status",
        "git diff",
        "git log",
        "git branch",
        "git remote -v",
        "git init",
        "git add ",
        "git commit ",
        "git push ",
    ),
    # Block shell chaining, redirection and
    # common destructive command patterns.
    blocked_operators=(
        ";",
        "&&",
        "||",
        "|",
        ">",
        "<",
        "`",
        "$(",
        "\n",
        "\r",
        "sudo ",
        "rm ",
        " --force",
        "--hard",
        "git clean",
        "git reset",
        "git push --force",
    ),
    timeout_seconds=60,
    max_memory_bytes=1024 * 1024 * 1024,
    max_file_size_bytes=1024 * 1024 * 20,
    max_child_processes=10,
)


shell_tool = ExecuteBashTool(
    workspace=WORKSPACE_PATH,
    policy=shell_policy,
)


# ----------------------------------
# 4. Filesystem MCP Server
# ----------------------------------

filesystem_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                WORKSPACE_PATH,
            ],
        )
    )
)


# ----------------------------------
# 5. GitHub MCP Server
# ----------------------------------

github_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {github_token}",
        },
    )
)


# ----------------------------------
# 6. GitHub Publisher Agent
# ----------------------------------

root_agent = Agent(
    name="github_publisher",
    model="gemini-3.5-flash",
    description=(
        "Coding assistant that creates projects, "
        "executes restricted shell commands and "
        "publishes code to GitHub."
    ),
    instruction=f"""
You are a coding and GitHub publishing assistant.

Your workspace is:

{WORKSPACE_PATH}

You have three capabilities:

1. FILESYSTEM
   - Read, create and edit project files.
   - Work only inside the assigned workspace.
   - Use absolute paths for filesystem operations.

2. SHELL
   - Execute permitted shell commands.
   - Run Python scripts and development commands.
   - Install project dependencies using uv or npm.
   - Run tests and inspect their output.
   - Use Git to inspect, commit and push changes.

3. GITHUB
   - Create and manage repositories.
   - Push project code.
   - Manage GitHub workflows using available MCP tools.

IMPORTANT RULES:

- Always work inside the assigned workspace.
- Never access or modify files outside the workspace.
- Never use destructive commands.
- Never attempt to bypass shell restrictions.
- Never use force push.
- Never delete files or repositories.
- Inspect Git status and diffs before committing.
- Ask the user before committing or pushing code.
- Never expose API keys, tokens or secrets.
- Do not put secrets inside generated project files.
- Verify command output before reporting success.

You must request user confirmation for shell execution
whenever the Bash tool requires it.
""",
    tools=[
        filesystem_toolset,
        shell_tool,
        github_toolset,
    ],
)
