"""Parallel Research Agent - Runs URL finder and article search in parallel."""

from google.adk.agents import ParallelAgent
from .url_finder_agent import url_finder_agent
from .article_agent import article_agent

# Create parallel agent for URL finder and article research
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    description=(
        "Runs URL finder search (for social media, personal web pages, etc.) and article search "
        "in parallel for a radiologist. After both agents complete and return their results, "
        "the workflow will proceed to the formatter agent to compile everything into a markdown profile."
    ),
    sub_agents=[url_finder_agent, article_agent],
)

