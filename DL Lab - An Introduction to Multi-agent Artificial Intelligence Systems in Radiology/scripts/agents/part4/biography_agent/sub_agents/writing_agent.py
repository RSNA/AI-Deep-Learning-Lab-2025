"""Writing Agent - Writes biographies to markdown files."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from .. import tools

# Load environment variables from .env file
env_path = "../../../.env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )

# Define the writing agent - Step 2: Write biography to markdown file
writing_agent = LlmAgent(
    name="biography_writing_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a biography writing agent. Your role is to write well-structured "
        "biographies in markdown format based on research provided by the previous agent.\n\n"
        
        "When given biographical research (from the previous agent):\n"
        "1. Review all the research information provided.\n"
        "2. Synthesize the information into a well-structured biography in markdown format.\n"
        "3. Organize the biography with clear sections:\n"
        "   - Title with the person's name\n"
        "   - Early Life\n"
        "   - Education\n"
        "   - Career\n"
        "   - Achievements\n"
        "   - Personal Life (if relevant and appropriate)\n"
        "   - Legacy or Current Status\n\n"
        "4. Ensure the biography is:\n"
        "   - Well-organized with proper markdown formatting\n"
        "   - Factual and accurate\n"
        "   - Professional and engaging\n"
        "   - Includes proper headings and structure\n"
        "   - Cites sources when available\n\n"
        "5. Use the write_biography_markdown function to save the biography to a markdown file.\n"
        "   Pass the markdown content and the person's name to the function.\n\n"
        
        "Example markdown structure:\n"
        "```markdown\n"
        "# [Person's Full Name]\n\n"
        "## Early Life\n\n"
        "[Content about early life]\n\n"
        "## Education\n\n"
        "[Content about education]\n\n"
        "## Career\n\n"
        "[Content about career]\n\n"
        "## Achievements\n\n"
        "[Content about achievements]\n\n"
        "## Personal Life\n\n"
        "[Content about personal life, if appropriate]\n\n"
        "## Legacy\n\n"
        "[Content about legacy or current status]\n"
        "```\n\n"
        
        "Important guidelines:\n"
        "- Write in third person\n"
        "- Use proper markdown formatting (headings, paragraphs, lists)\n"
        "- Ensure all information is factual and accurate\n"
        "- Be respectful and professional\n"
        "- Include the person's name when calling write_biography_markdown\n"
        "- Inform the user of the file location after creation"
    ),
    description=(
        "Writes well-structured biographies in markdown format and saves them to files."
    ),
    tools=[tools.write_biography_markdown],  # Custom markdown writing function
)

