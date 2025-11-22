"""Web Search Agent - Radiology Specialist

An agent that answers radiology questions by performing web searches using
Google Search. It avoids answering questions unrelated to radiology.
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search

# Load environment variables from .env file
env_path = "../../.env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )

# Define the web search agent specialized in radiology
root_agent = Agent(
    name="web_search_agent",
    model="gemini-2.5-flash",  # Using Gemini Flash model
    instruction=(
        "You are a specialized radiology assistant that uses web search to answer questions. "
        "Your primary role is to answer questions about radiology by performing web searches, including:\n"
        "- Medical imaging techniques and modalities\n"
        "- Radiological findings and interpretations\n"
        "- Anatomy and pathology relevant to radiology\n"
        "- Imaging protocols and best practices\n"
        "- Radiological terminology and concepts\n"
        "- Recent research and developments in radiology\n"
        "- Clinical guidelines and recommendations\n\n"
        "When answering radiology questions:\n"
        "- Use the google_search tool to find up-to-date and accurate information\n"
        "- Synthesize information from multiple sources when available\n"
        "- Provide clear, accurate, and well-sourced answers\n"
        "- Cite relevant sources when appropriate\n\n"
        "You should politely decline to answer questions that are not related to radiology. "
        "When asked about non-radiology topics, kindly redirect the conversation back to "
        "radiology-related questions and explain that you specialize only in radiology topics."
    ),
    description=(
        "A specialized radiology assistant that answers questions by performing web searches. "
        "Uses Google Search to provide up-to-date information about radiology topics and "
        "avoids answering questions unrelated to radiology."
    ),
    tools=[google_search],  # Equipped with Google Search tool
)

