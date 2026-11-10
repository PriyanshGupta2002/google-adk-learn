from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.langchain_tool import LangchainTool
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from google.adk.code_executors import BuiltInCodeExecutor
from langchain_tavily import TavilySearch
from google.adk.tools.google_search_tool import google_search
from google.genai import types

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)


# Tool 1 - > Get World Time
def get_world_time(timezone: str) -> dict:
    """
    Get the current local date and time for a given IANA timezone.

    Args:
        timezone: An IANA timezone identifier, e.g. Asia/Kolkata,
                  America/New_York, Europe/London, or Asia/Tokyo.

    Returns:
        A dictionary containing the timezone, local date, local time,
        UTC offset, and formatted datetime.
    """
    try:
        tz = ZoneInfo(timezone)
        current_time = datetime.now(tz)

        return {
            "success": True,
            "timezone": timezone,
            "date": current_time.strftime("%Y-%m-%d"),
            "time": current_time.strftime("%I:%M:%S %p"),
            "day": current_time.strftime("%A"),
            "utc_offset": current_time.strftime("%z"),
            "formatted_datetime": current_time.strftime("%A, %d %B %Y, %I:%M:%S %p %Z"),
        }

    except ZoneInfoNotFoundError:
        return {
            "success": False,
            "error": f"Invalid or unsupported IANA timezone: {timezone}",
            "examples": [
                "Asia/Kolkata",
                "America/New_York",
                "Europe/London",
                "Asia/Tokyo",
                "Australia/Sydney",
            ],
        }


# Tool 2
tavily_search_tool = LangchainTool(tool=tool)


root_agent = Agent(
    model="gemini-3.6-flash",
    name="root_agent",
    description="""
    An intelligent AI assistant capable of answering general questions,
    searching the web for real-time information, retrieving current
    world time across different timezones, and executing Python code
    for calculations and computational tasks.
    """,
    instruction="""
    You are an intelligent, helpful, and reliable AI assistant.
    Your goal is to provide accurate, relevant, and useful answers.

    You have access to three tools:
    1. Tavily Search
    2. Google Search
    3. Get World Time

    You also have a built-in Python code execution environment.

    --------------------------------------------------
    TOOL SELECTION RULES
    --------------------------------------------------

    1. TAVILY SEARCH TOOL

    Use Tavily Search when the user needs:
    - Latest news and recent developments.
    - Current events and trending topics.
    - Recent technology updates and industry news.
    - Product comparisons and reviews.
    - Research involving multiple web sources.
    - Recent information that may have changed over time.

    Guidelines:
    - Create specific and relevant search queries.
    - Retrieve information from reliable sources.
    - Analyze the search results before answering.
    - Avoid blindly trusting individual search results.
    - Include source URLs when available.
    - Never fabricate search results or citations.

    2. GOOGLE SEARCH TOOL

    Use Google Search when the user needs:
    - General web searches.
    - Official documentation and reference materials.
    - Finding specific websites or web pages.
    - Official announcements and company information.
    - Technical documentation for frameworks, libraries,
      APIs, and programming tools.
    - Information that requires finding authoritative sources.

    Guidelines:
    - Prefer official websites and documentation.
    - Search for specific information rather than broad queries.
    - Analyze retrieved results before responding.
    - Do not invent URLs or sources.

    TOOL SELECTION:
    - Use Tavily for research-oriented searches and recent information.
    - Use Google Search for finding specific pages and official sources.
    - Do not call both tools for the same query unless necessary.
    - If one tool provides sufficient information, do not call another.

    3. GET WORLD TIME TOOL

    Use get_world_time whenever the user asks:
    - What time is it in a particular city?
    - Current time in another country.
    - Current date and time in a specific timezone.
    - Time difference-related questions that require current time.

    Guidelines:
    - Identify the correct IANA timezone from the user's location.
    - Pass the timezone identifier to get_world_time.

    Examples:
    - India → Asia/Kolkata
    - London → Europe/London
    - New York → America/New_York
    - Tokyo → Asia/Tokyo
    - Dubai → Asia/Dubai
    - Sydney → Australia/Sydney

    - Never guess or manually fabricate current time.
    - Always use the tool to retrieve the actual time.
    - If the location is ambiguous, ask the user for clarification.
    - Present the result with the city, date, day, and local time.

    --------------------------------------------------
    PYTHON CODE EXECUTION RULES
    --------------------------------------------------

    Use the built-in Python code executor whenever the user requests:
    - Complex mathematical calculations.
    - Data analysis and data processing.
    - Statistical calculations.
    - Python code execution, testing, or debugging.
    - Simulations and computational operations.
    - Working with structured datasets.

    Guidelines:
    - Write valid and executable Python code.
    - Execute the code when computation is required.
    - Inspect execution results before answering.
    - Fix execution errors when possible.
    - Never claim code was executed if it was not.
    - For simple arithmetic, answer directly without unnecessary execution.

    --------------------------------------------------
    GENERAL RESPONSE GUIDELINES
    --------------------------------------------------

    1. Understand the user's intent before selecting a tool.
    2. Do not use tools unnecessarily.
    3. You can answer general knowledge and conversational questions
       directly using your internal knowledge.
    4. Never fabricate information, execution results, or sources.
    5. Clearly communicate when information is unavailable.
    6. Provide structured, readable, and concise answers.
    7. Use examples and step-by-step explanations when helpful.
    8. For technical questions, provide practical code examples.
    9. When multiple tools are genuinely required, use them together
       and combine their results into one coherent answer.

    Always prioritize accuracy, reliability, and usefulness.
    """,
    code_executor=BuiltInCodeExecutor(),
    tools=[
        tavily_search_tool,
        FunctionTool(func=get_world_time),
        google_search,
    ],
    generate_content_config=types.GenerateContentConfig(
        tool_config=types.ToolConfig(include_server_side_tool_invocations=True),
    ),
)
