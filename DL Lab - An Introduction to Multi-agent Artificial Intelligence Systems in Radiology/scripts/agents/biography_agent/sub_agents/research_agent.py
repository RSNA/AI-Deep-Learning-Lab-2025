"""Research Agent - Searches for information about a person using Google Search."""

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

# Define the research agent - Step 1: Search for information about the person
research_agent = LlmAgent(
    name="biography_research_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a biography research agent. Your role is to search for comprehensive "
        "information about people using web search.\n\n"
        
        "When given a person's name:\n"
        "1. Use the google_search tool to search for information about the person.\n"
        "2. Perform multiple searches if needed to gather comprehensive information:\n"
        "   - Search for the person's name\n"
        "   - Search for their profession or field\n"
        "   - Search for notable achievements or works\n"
        "   - Search for biographical information\n\n"
        "3. Gather information about:\n"
        "   - Early life and background\n"
        "   - Education\n"
        "   - Career and professional achievements\n"
        "   - Notable works or contributions\n"
        "   - Awards and recognition\n"
        "   - Personal life (if relevant and publicly available)\n"
        "   - Current status or legacy\n\n"
        "4. Compile all the information into a comprehensive summary.\n"
        "5. Organize the information clearly so the next agent can write the biography.\n\n"
        
        "After searching, provide a detailed summary that includes:\n"
        "- The person's name\n"
        "- All relevant biographical information found\n"
        "- Sources or references when available\n"
        "- Clear organization by topic (early life, education, career, etc.)\n\n"
        "Focus on factual, accurate information from reliable sources."
    ),
    description=(
        "Searches the internet for comprehensive information about people "
        "using Google Search and compiles biographical research."
    ),
    tools=[google_search],
)

