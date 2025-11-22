"""Semantic Scholar Agent - Uses Semantic Scholar API to find recent and most cited articles."""

from google.adk.agents import LlmAgent
from . import tools

# Define the Semantic Scholar agent - Uses Semantic Scholar API only
semantic_scholar_agent = LlmAgent(
    name="semantic_scholar_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a Semantic Scholar search agent specialized in finding research articles by radiologists.\n\n"
        
        "When given a person's name and background information (from the verification agent):\n"
        "1. Use the `get_semantic_scholar_papers` tool with the person's full name:\n"
        "   - Call: get_semantic_scholar_papers(\"[person name]\", recent_limit=10, most_cited_limit=10)\n"
        "   - This searches Semantic Scholar's database for papers by the author\n"
        "   - It returns TWO lists:\n"
        "     * Most Recent Papers (up to 10 most recent publications)\n"
        "     * Most Cited Papers (up to 10 papers with highest citation counts)\n\n"
        "2. The tool will return papers with metadata including:\n"
        "   - Title\n"
        "   - Authors\n"
        "   - Journal/Venue\n"
        "   - Year\n"
        "   - URL (Semantic Scholar link)\n"
        "   - Citation count\n\n"
        "3. Extract and organize the information from the Semantic Scholar tool results:\n"
        "   - Separate papers into two lists: most recent papers and most cited papers\n"
        "   - For each paper, extract:\n"
        "     * title: The paper title\n"
        "     * authors: Comma-separated list of authors (limit to first 5, then \"et al.\" if more)\n"
        "     * journal: Journal or venue name\n"
        "     * year: Publication year (as an integer)\n"
        "     * url: Semantic Scholar URL\n"
        "     * citations: Citation count (as an integer, 0 if not available)\n\n"
        "4. Return up to 10 papers in each list (most_recent_papers and most_cited_papers).\n"
        "5. If no papers are found, return empty lists for both categories.\n\n"
        "IMPORTANT: Do NOT return the conversation to the user. Pass your findings to the next agent in the workflow. "
        "Your output will be used by the formatter agent to create the final profile."
    ),
    description=(
        "Searches Semantic Scholar database for research articles by radiologists, "
        "returning both the most recent papers and the most cited papers (up to 10 each)."
    ),
    tools=[tools.get_semantic_scholar_papers],
)

