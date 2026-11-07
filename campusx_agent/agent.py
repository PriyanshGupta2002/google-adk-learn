from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# root_agent = Agent(
#     model=LiteLlm(model="openrouter/anthropic/claude-sonnet-4"),
#     name="root_agent",
#     description="A helpful assistant for user questions.",
#     instruction="Answer user questions to the best of your knowledge",
# )


root_agent = Agent(
    model=LiteLlm(model="openrouter/qwen/qwen3.8-27b"),
    name="root_agent",
    description="A helpful assistant for user questions.",
    instruction="Answer user questions to the best of your knowledge",
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3, max_output_tokens=800
    ),
)
