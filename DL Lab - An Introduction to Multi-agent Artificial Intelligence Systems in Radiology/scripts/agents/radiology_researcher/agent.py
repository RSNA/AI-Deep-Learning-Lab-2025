"""Radiology Researcher Agent - Sequential Agent Version

This agent uses a sequential workflow with two specialized agents:
1. Search Agent: Uses Google Search to find top radiology guidelines
2. Processing Agent: Uses Firecrawl MCP to crawl URLs and generate CSV files

This approach separates concerns and avoids the limitation of mixing function calling
with MCP tools in a single agent.
"""

from google.adk.agents import SequentialAgent
from .sub_agents import search_agent, processing_agent

# Create sequential workflow: Search first, then process
root_agent = SequentialAgent(
    name="radiology_researcher",
    description=(
        "A sequential workflow that finds radiology guidelines using Google Search, "
        "then extracts metadata using Firecrawl MCP and compiles results into CSV files. "
        "Focuses on authoritative radiology guidelines and clinical recommendations."
    ),
    sub_agents=[search_agent, processing_agent],
)

