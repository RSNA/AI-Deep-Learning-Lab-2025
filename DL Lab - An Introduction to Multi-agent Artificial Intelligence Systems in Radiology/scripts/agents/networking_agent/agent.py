"""Networking Agent - Complex Multi-Agent System

This agent creates networking profiles for radiologists using a sophisticated workflow:
1. Verification Agent: Checks if person is a radiologist and gathers background
2. Parallel Research Agent: Runs URL finder and article search in parallel
   - URL Finder Agent: Finds social media, personal web pages, and other publicly available URLs (Google Search)
   - Article Agent: Finds recent articles and extracts metadata (title, journal, year, URL) from Google Search results
3. Formatter Agent: Compiles everything into a markdown profile

This demonstrates hierarchical multi-agent systems with sequential and parallel workflows.
"""

from google.adk.agents import SequentialAgent
from .sub_agents import verification_agent, parallel_research_agent, formatter_agent

# Create sequential workflow: Verify -> Parallel Research -> Format
root_agent = SequentialAgent(
    name="networking_agent",
    description=(
        "A comprehensive networking agent that creates profiles for radiologists. "
        "Verifies radiologist status, finds URLs (social media, personal pages) and recent articles in parallel, "
        "then compiles everything into a professional markdown profile."
    ),
    sub_agents=[
        verification_agent,      # Step 1: Verify radiologist and get background
        parallel_research_agent, # Step 2: Find URLs and articles in parallel
        formatter_agent,         # Step 3: Compile into markdown
    ],
)

