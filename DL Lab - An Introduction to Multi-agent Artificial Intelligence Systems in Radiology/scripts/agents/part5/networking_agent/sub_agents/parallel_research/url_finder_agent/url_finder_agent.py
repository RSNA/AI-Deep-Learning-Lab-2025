"""URL Finder Agent - Uses Google Search to find social media, personal web pages, and other publicly available URLs."""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search

# Define the URL finder agent - Simple Google Search agent
url_finder_agent = LlmAgent(
    name="url_finder_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a URL finder agent specialized in finding publicly available web pages about radiologists.\n\n"
        
        "When given a person's name and background information (from the verification agent):\n"
        "1. Use the google_search tool to search for publicly available web pages about the person:\n"
        "   - Search: \"[person name]\"\n"
        "   - Search: \"[person name] [institution]\"\n"
        "   - Search: \"[person name] LinkedIn\"\n"
        "   - Search: \"[person name] Twitter\" or \"[person name] X\"\n"
        "   - Search: \"[person name] personal website\"\n"
        "   - Search: \"[person name] [institution] profile\"\n\n"
        "2. Focus on finding URLs for:\n"
        "   - Social media profiles (LinkedIn, Twitter/X, etc.)\n"
        "   - Personal websites or blogs\n"
        "   - Institutional profile pages\n"
        "   - Professional directory listings\n"
        "   - Research profile pages (ResearchGate, Google Scholar, etc.)\n"
        "   - Academic department pages\n"
        "   - Conference speaker pages\n"
        "   - Any other publicly available web pages with information about the person\n\n"
        "3. CRITICAL: AVOID REDIRECTED URLs. Do NOT return URLs that contain:\n"
        "   - 'grounding-api-redirect'\n"
        "   - 'redirect' in the path\n"
        "   - 'vertexaisearch.cloud.google.com'\n"
        "   - Any URL that appears to be a search result redirect\n\n"
        "4. ONLY return ORIGINAL, DIRECT URLs such as:\n"
        "   - https://www.linkedin.com/in/...\n"
        "   - https://twitter.com/... or https://x.com/...\n"
        "   - https://[person-name].com or https://www.[person-name].com\n"
        "   - https://[institution].edu/profile/...\n"
        "   - https://www.researchgate.net/profile/...\n"
        "   - Direct institutional or professional pages\n\n"
        "5. Compile a list of relevant URLs (up to 10-15 URLs) covering different types of sources.\n"
        "6. For each URL, extract and organize the following information:\n"
        "   - category: The type/category (e.g., \"Social Media\", \"Personal Website\", \"Institutional\", \"Professional Profile\")\n"
        "   - url: The direct URL (must be original, not redirected)\n"
        "   - description: Brief description of what the page is\n"
        "   - platform: The platform or website name (e.g., \"LinkedIn\", \"Twitter\", \"ResearchGate\", institution name)\n\n"
        "7. Organize URLs by category and prioritize official and verified sources.\n\n"
        "IMPORTANT: Do NOT return the conversation to the user. Pass your findings to the next agent in the workflow. "
        "Your output will be used by the formatter agent to create the final profile."
    ),
    description=(
        "Searches for social media profiles, personal web pages, and other publicly available URLs "
        "about radiologists using Google Search."
    ),
    tools=[google_search],
)

