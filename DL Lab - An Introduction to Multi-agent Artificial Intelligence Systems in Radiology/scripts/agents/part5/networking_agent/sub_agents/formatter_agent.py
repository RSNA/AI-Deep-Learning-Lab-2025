"""Formatter Agent - Compiles all information into a structured networking profile."""

from pydantic import BaseModel
from typing import Optional, List
from google.adk.agents import LlmAgent

# Define Pydantic models for structured output
class Paper(BaseModel):
    title: str
    journal: str
    year: int
    url: str
    citations: int
    authors: str


class PublicationSection(BaseModel):
    most_recent_papers: List[Paper]
    most_cited_papers: List[Paper]


class URLInfo(BaseModel):
    category: str
    url: str
    description: str
    platform: str


class NetworkingProfile(BaseModel):
    person_name: str
    background: str
    online_presence: List[URLInfo]
    recent_publications: PublicationSection
    contact_information: Optional[str] = None


# Define the formatter agent - Step 3: Compile everything into structured output
formatter_agent = LlmAgent(
    name="profile_formatter_agent",
    model="gemini-2.5-flash",
    output_schema=NetworkingProfile,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    instruction=(
        "You are a profile formatting agent. Your role is to compile all gathered information "
        "into a structured networking profile.\n\n"
        
        "When given information from previous agents:\n"
        "1. Review all information provided:\n"
        "   - Background information from verification agent\n"
        "   - URLs from URL finder agent (social media, personal web pages, etc.)\n"
        "   - Recent articles from article agent (including Most Recent Papers and Most Cited Papers sections)\n\n"
        "2. Extract and structure the information according to the required format:\n"
        "   - person_name: The full name of the person\n"
        "   - background: Background information from verification agent (clear, professional format)\n"
        "   - online_presence: List of URLInfo objects with:\n"
        "     * category: Type (e.g., \"Social Media\", \"Personal Website\", \"Institutional\")\n"
        "     * url: The direct URL\n"
        "     * description: Brief description of the page\n"
        "     * platform: Platform or website name (e.g., \"LinkedIn\", \"Twitter\", institution name)\n"
        "   - recent_publications: PublicationSection with:\n"
        "     * most_recent_papers: List of Paper objects (up to 10)\n"
        "     * most_cited_papers: List of Paper objects (up to 10)\n"
        "     Each Paper should have: title, journal, year (integer), url, citations (integer), authors\n"
        "   - contact_information: Contact info if available from background research (optional)\n\n"
        "3. Structure the response according to the NetworkingProfile schema.\n"
        "4. Ensure all data is accurate and well-organized.\n"
        "5. Return the structured profile - this will be returned to the user.\n\n"
        "IMPORTANT: Return the structured profile according to the NetworkingProfile schema. "
        "Do NOT save any files - just return the structured data."
    ),
    description=(
        "Compiles all gathered information (background, URLs, articles) into a "
        "structured networking profile using Pydantic models."
    ),
    tools=[],
)

