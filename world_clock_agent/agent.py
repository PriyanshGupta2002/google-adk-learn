from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool


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


root_agent = Agent(
    model="gemini-3.5-flash",
    name="root_agent",
    description=(
        "A helpful AI assistant that can answer general questions "
        "and retrieve the current local time for cities worldwide."
    ),
    instruction="""
    You are a helpful AI assistant with access to a world-time tool.

    WORLD TIME INSTRUCTIONS:

    1. Whenever the user asks for the current time in a city,
       country, or region, use the get_world_time tool.

    2. Identify the appropriate IANA timezone from the user's query.

       Examples:
       - India → Asia/Kolkata
       - London → Europe/London
       - New York → America/New_York
       - Tokyo → Asia/Tokyo
       - Dubai → Asia/Dubai
       - Sydney → Australia/Sydney

    3. Pass the IANA timezone identifier to get_world_time.

    4. Never calculate or guess the current time yourself.
       Always use the tool to retrieve the actual time.

    5. If a city has multiple possible timezones or the location
       is ambiguous, ask the user for clarification.

    6. Present the returned time in a friendly, readable format.
       Include the city, date, day, and local time.

    7. Do not call the tool for questions about historical times
       or general timezone explanations.

    GENERAL INSTRUCTIONS:
    - Answer accurately and clearly.
    - Keep responses concise.
    - Never fabricate tool results.
    """,
    tools=[FunctionTool(func=get_world_time)],
)
