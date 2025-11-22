"""Biography Agent - BROKEN VERSION

This agent demonstrates the unsupported pattern of mixing Google Search tool
with custom function tools in a single agent. This will not work properly.

The agent receives a person's name, searches the internet, and writes a biography
in a markdown file - all in one agent (which is the broken pattern).
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search
from . import tools

# Load environment variables from .env file
env_path = "../../.env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )

# Define the biography agent - BROKEN: mixing Google Search with custom function tool
root_agent = Agent(
    name="biography_agent_broken",
    model="gemini-2.5-flash",
    instruction=(
        "You are a biography writer agent. Your role is to research people and write their biographies.\n\n"
        
        "When given a person's name:\n"
        "1. Use the google_search tool to search for information about the person.\n"
        "2. Gather comprehensive information including:\n"
        "   - Early life and background\n"
        "   - Education\n"
        "   - Career and achievements\n"
        "   - Notable works or contributions\n"
        "   - Personal life (if relevant and publicly available)\n"
        "   - Awards and recognition\n"
        "   - Current status or legacy\n\n"
        "3. Synthesize the information into a well-structured biography in markdown format.\n"
        "4. Use the write_biography_markdown function to save the biography to a markdown file.\n\n"
        
        "The biography should be:\n"
        "- Well-organized with clear sections\n"
        "- Factual and accurate\n"
        "- Properly formatted in markdown\n"
        "- Include sources when possible\n"
        "- Professional and engaging\n\n"
        
        "Example markdown structure:\n"
        "# [Person's Name]\n\n"
        "## Early Life\n\n"
        "## Education\n\n"
        "## Career\n\n"
        "## Achievements\n\n"
        "## Personal Life\n\n"
        "## Legacy\n\n"
    ),
    description=(
        "A biography writer that searches the internet for information about people "
        "and writes their biographies in markdown files. "
        "BROKEN: This agent mixes Google Search tool with custom function tools in a single agent."
    ),
    tools=[
        google_search,  # Google Search tool
        tools.write_biography_markdown,  # Custom markdown writing function
    ],
)

