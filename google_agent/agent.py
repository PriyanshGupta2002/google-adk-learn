from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import google_search

root_agent = Agent(
    model="gemini-3.8-flash",
    name="root_agent",
    description="A helpful assistant that searches the web.",
    instruction="""
    Answer the user questions accurately use the google search when you need it 
    for current information or want to verify any fact
""",
    tools=[google_search],
)
