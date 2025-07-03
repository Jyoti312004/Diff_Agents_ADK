from google.adk.agents import Agent
from google.adk.tools import google_search

# we can't use custom tools with adk provided tools

def get_current_time():
    """ Returns the current time in a formatted string.
    This function can be used as a tool in the agent.
    It returns the current time in the format 'YYYY-MM-DD HH:MM:SS'."""
    print("***** hi i am a tool *****")
    from datetime import datetime

    return {"current_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

root_agent = Agent(
    name="tool_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get_current_time
    """,
    tools=[get_current_time],
      # tools=[google_search],
)