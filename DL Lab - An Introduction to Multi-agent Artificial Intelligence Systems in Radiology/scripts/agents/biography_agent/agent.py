"""Biography Agent - Fixed Sequential Version

This agent uses a sequential workflow with two specialized agents:
1. Research Agent: Uses Google Search to find information about a person
2. Writing Agent: Writes the biography to a markdown file

This approach separates concerns and avoids the limitation of mixing function calling
with Google Search tools in a single agent.
"""

from google.adk.agents import SequentialAgent
from .sub_agents import research_agent, writing_agent

# Create sequential workflow: Research first, then write
root_agent = SequentialAgent(
    name="biography_agent",
    description=(
        "A sequential workflow that researches people using Google Search, "
        "then writes their biographies in markdown files. "
        "Uses separate agents for research and writing to avoid tool conflicts."
    ),
    sub_agents=[research_agent, writing_agent],
)

