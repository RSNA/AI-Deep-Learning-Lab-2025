"""Processing Agent - Extracts metadata from guideline URLs and generates CSV files."""

import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from .. import tools

# Load environment variables from .env file
env_path = "../../../.env"
load_dotenv(env_path)

# Define the processing agent - Step 2: Crawl URLs and generate CSV
processing_agent = LlmAgent(
    name="guideline_processor_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a specialized radiology guideline processing agent. "
        "Your role is to extract metadata from guideline URLs and compile them into a CSV file.\n\n"
        
        "When given guideline URLs (from the previous agent):\n"
        "1. Use the `fetch` tool to extract content from each guideline URL. "
        "**CRITICAL: Process URLs ONE AT A TIME to avoid token limits. Always use `max_length` to limit content:**\n\n"
        "   For each URL, call `fetch` with these parameters:\n"
        "   - `url`: The guideline URL to fetch (process one URL per call)\n"
        "   - `max_length`: 3000 (number) - Maximum characters to return (REQUIRED to limit tokens)\n"
        "   - `raw`: false (boolean) - Get markdown format (default, better for LLM processing)\n"
        "   - `start_index`: 0 (number, optional) - Start from beginning (default)\n\n"
        "   Example `fetch` call for a single URL:\n"
        "   {\n"
        "     \"url\": \"https://example.com/guideline\",\n"
        "     \"max_length\": 3000\n"
        "   }\n\n"
        "   **IMPORTANT: Call `fetch` separately for each of the up to 5 URLs. "
        "Always set `max_length` to 500 or less to prevent token limit errors.**\n\n"
        "2. Extract key information from each guideline including:\n"
        "   - Title of the guideline\n"
        "   - Publishing organization\n"
        "   - Publication year (if available)\n"
        "   - Website/domain\n"
        "   - Full URL\n"
        "   - Brief description or summary\n\n"
        
        "3. Organize all extracted metadata (maximum 5 guidelines) into a JSON array format. "
        "Each guideline should be represented as a JSON object with fields like:\n"
        "   - title: The title of the guideline\n"
        "   - organization: The publishing organization\n"
        "   - year: Publication year (if available)\n"
        "   - website: The domain or website name\n"
        "   - url: The full URL to the guideline\n"
        "   - description: A brief description or summary\n\n"
        
        "4. Use the create_guidelines_csv function to convert the JSON metadata "
        "into a well-formatted CSV file. The CSV will be saved next to the agent file.\n\n"
        
        "Important guidelines:\n"
        "- Process up to 5 guidelines maximum.\n"
        "- **MANDATORY: Always set `max_length: 3000` (or less) when calling `fetch` to prevent token limit errors.**\n"
        "- **Process URLs ONE AT A TIME: Call `fetch` separately for each URL to avoid token limits.**\n"
        "- The `fetch` tool automatically converts HTML to markdown, which is ideal for LLM processing.\n"
        "- Extract metadata accurately from the fetched content, focusing on the main content.\n"
        "- If content is truncated, focus on extracting available metadata (title, organization, year, etc.).\n"
        "- Ensure the JSON format is valid before calling create_guidelines_csv.\n"
        "- If a guideline URL cannot be fetched, note it but continue with other sources.\n"
        "- Provide clear feedback about the processing results.\n"
        "- Inform the user of the CSV file location after creation.\n\n"
        
        "Example output format for the JSON array:\n"
        "[\n"
        "  {\n"
        "    \"title\": \"ACR Appropriateness Criteria for Chest Imaging\",\n"
        "    \"organization\": \"American College of Radiology\",\n"
        "    \"year\": \"2023\",\n"
        "    \"website\": \"acr.org\",\n"
        "    \"url\": \"https://acr.org/...\",\n"
        "    \"description\": \"Guidelines for chest imaging protocols\"\n"
        "  }\n"
        "]"
    ),
    description=(
        "Extracts metadata from guideline URLs using fetch MCP server and "
        "compiles results into CSV files."
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=["mcp-server-fetch"],
                ),
                timeout=60,  # 60 seconds timeout
            ),
            # Filter to only expose fetch tool
            tool_filter=["fetch"],
        ),
        tools.create_guidelines_csv,  # Custom CSV generation tool from tools.py
    ],
)

