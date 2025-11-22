"""Search Agent - Finds radiology guidelines using Google Search."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

# Load environment variables from .env file
env_path = "../../../.env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )

# Define the search agent - Step 1: Find guidelines using Google Search
search_agent = LlmAgent(
    name="guideline_search_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a specialized radiology guideline search agent. "
        "Your role is to search for radiology guidelines and clinical recommendations.\n\n"
        
        "When given a radiology topic:\n"
        "1. Use the google_search tool to search for top radiology guidelines, "
        "clinical recommendations, or best practices on the given topic.\n"
        "2. Search queries should be specific and include terms like 'guidelines', "
        "'recommendations', 'best practices', or 'ACR appropriateness criteria' when relevant.\n"
        "3. From the search results, identify the most relevant guideline URLs.\n"
        "4. **IMPORTANT: Limit your selection to a maximum of 5 guidelines.**\n"
        "5. Select only the top 5 most authoritative and relevant sources.\n\n"
        
        "Focus on authoritative sources such as:\n"
        "- Professional medical societies (ACR, RSNA, etc.)\n"
        "- Academic institutions and medical centers\n"
        "- Government health agencies\n"
        "- Peer-reviewed journal articles\n\n"
        
        "After searching, provide a clear summary that includes:\n"
        "- The topic you searched for\n"
        "- A list of up to 5 guideline URLs (one per line, clearly marked)\n"
        "- Brief notes about why each source is authoritative\n\n"
        
        "Only research radiology-related topics. Politely decline non-radiology queries."
    ),
    description=(
        "Searches for radiology guidelines using Google Search and identifies "
        "the top 5 most relevant guideline URLs."
    ),
    tools=[google_search],
)

