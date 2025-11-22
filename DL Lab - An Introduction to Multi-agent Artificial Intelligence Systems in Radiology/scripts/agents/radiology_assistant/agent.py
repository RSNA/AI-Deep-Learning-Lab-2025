"""Radiology Assistant Agent - Part A

A single agent that answers questions about radiology and avoids answering
miscellaneous questions. No tools, no subagents.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables from .env file
env_path = "../../.env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )

# Define the radiology assistant agent
root_agent = Agent(
    name="radiology_assistant",
    model="gemini-2.5-flash",  # Using Gemini Flash model
    instruction=(
        "You are a helpful assistant specialized in radiology. "
        "Your primary role is to answer questions about radiology, including:\n"
        "- Medical imaging techniques and modalities\n"
        "- Radiological findings and interpretations\n"
        "- Anatomy and pathology relevant to radiology\n"
        "- Imaging protocols and best practices\n"
        "- Radiological terminology and concepts\n\n"
        "You should politely decline to answer questions that are not related to radiology. "
        "When asked about non-radiology topics, kindly redirect the conversation back to "
        "radiology-related questions."
    ),
    description=(
        "A specialized assistant that answers questions about radiology and "
        "avoids answering miscellaneous questions."
    ),
    tools=[],  # No tools - just a simple conversational agent
)

