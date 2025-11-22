"""Main script to run the networking agent and generate markdown profile."""

import sys
import json
import uuid
import os
from pathlib import Path
from dotenv import load_dotenv
from agents.networking_agent.agent import root_agent
from agents.networking_agent.sub_agents.formatter_agent import NetworkingProfile
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.runners import types
import asyncio

# Load environment variables from .env file in the same directory as main.py
env_path = ".env"
load_dotenv(env_path)

# Ensure API key is loaded
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENAI_API_KEY")
if not api_key:
    raise ValueError(
        "Please set GOOGLE_API_KEY or GOOGLE_GENAI_API_KEY in your .env file"
    )


def profile_to_markdown(profile: NetworkingProfile) -> str:
    """Convert NetworkingProfile Pydantic model to markdown format.
    
    Args:
        profile: NetworkingProfile Pydantic model instance
    
    Returns:
        Formatted markdown string
    """
    markdown_parts = []
    
    # Header
    markdown_parts.append(f"# {profile.person_name} - Networking Profile\n")
    
    # Background
    markdown_parts.append("## Background\n")
    markdown_parts.append(f"{profile.background}\n")
    
    # Online Presence
    markdown_parts.append("## Online Presence\n")
    if profile.online_presence:
        # Group URLs by category
        categories = {}
        for url_info in profile.online_presence:
            category = url_info.category
            if category not in categories:
                categories[category] = []
            categories[category].append(url_info)
        
        # Write each category
        for category, urls in categories.items():
            markdown_parts.append(f"### {category}\n")
            for url_info in urls:
                markdown_parts.append(f"- [{url_info.platform}]({url_info.url}) - {url_info.description}\n")
    else:
        markdown_parts.append("No online presence information available.\n")
    markdown_parts.append("")
    
    # Recent Publications
    markdown_parts.append("## Recent Publications\n")
    
    # Most Recent Papers
    if profile.recent_publications.most_recent_papers:
        markdown_parts.append("### Most Recent Papers\n")
        for paper in profile.recent_publications.most_recent_papers:
            markdown_parts.append(
                f"- **{paper.title}** - *{paper.journal}* ({paper.year}) "
                f"[Link]({paper.url}) - Citations: {paper.citations}\n"
            )
        markdown_parts.append("")
    
    # Most Cited Papers
    if profile.recent_publications.most_cited_papers:
        markdown_parts.append("### Most Cited Papers\n")
        for paper in profile.recent_publications.most_cited_papers:
            markdown_parts.append(
                f"- **{paper.title}** - *{paper.journal}* ({paper.year}) "
                f"[Link]({paper.url}) - Citations: {paper.citations}\n"
            )
        markdown_parts.append("")
    
    # Contact Information
    if profile.contact_information:
        markdown_parts.append("## Contact Information\n")
        markdown_parts.append(f"{profile.contact_information}\n")
    
    return "".join(markdown_parts)


async def run_agent_async(person_name: str) -> NetworkingProfile:
    """Run the networking agent with a given person's name (async version).
    
    Args:
        person_name: The name of the person to research
    
    Returns:
        NetworkingProfile Pydantic model instance
    """
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a unique session ID
    session_id = str(uuid.uuid4())
    user_id = "user"
    app_name = "agents"
    
    # Create the session explicitly before running (as per ADK documentation)
    _ = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create runner with the root agent
    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service
    )
    
    # Create the message content
    message = types.Content(
        parts=[types.Part(text=f"Create a networking profile for {person_name}")],
        role="user"
    )
    
    # Run the agent and collect events using run_async
    events = []
    final_response_text = None
    
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            events.append(event)
            
            # Check if this is the final response (as per ADK documentation)
            if hasattr(event, 'is_final_response') and event.is_final_response():
                if hasattr(event, 'content') and event.content:
                    if hasattr(event.content, 'parts') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                final_response_text = part.text
                                # Try to parse as JSON (structured output)
                                try:
                                    data = json.loads(part.text)
                                    if isinstance(data, dict) and 'person_name' in data:
                                        return NetworkingProfile(**data)
                                except (json.JSONDecodeError, TypeError, ValueError):
                                    pass
            
            # Also check event.content for structured output
            if hasattr(event, 'content') and event.content:
                if hasattr(event.content, 'parts') and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            # Try to parse as JSON (structured output)
                            try:
                                data = json.loads(part.text)
                                if isinstance(data, dict) and 'person_name' in data:
                                    return NetworkingProfile(**data)
                            except (json.JSONDecodeError, TypeError, ValueError):
                                pass
    except Exception as e:
        print(f"Error during event processing: {e}")
        import traceback
        traceback.print_exc()
    
    # If we have a final response text but couldn't parse it, try one more time
    if final_response_text:
        try:
            data = json.loads(final_response_text)
            if isinstance(data, dict) and 'person_name' in data:
                return NetworkingProfile(**data)
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    
    # Debug: Print event types to help diagnose
    if events:
        print(f"Debug: Received {len(events)} events")
        print(f"Debug: Event types: {[type(e).__name__ for e in events[-5:]]}")
        if final_response_text:
            print(f"Debug: Final response text (first 500 chars): {final_response_text[:500]}")
    
    raise ValueError(f"Could not parse NetworkingProfile from agent response. "
                    f"Received {len(events)} events.")


def run_agent(person_name: str) -> NetworkingProfile:
    """Run the networking agent (synchronous wrapper for async function).
    
    Args:
        person_name: The name of the person to research
    
    Returns:
        NetworkingProfile Pydantic model instance
    """
    return asyncio.run(run_agent_async(person_name))


def save_markdown_file(markdown_content: str, person_name: str, output_dir: Path = None) -> Path:
    """Save markdown content to a file.
    
    Args:
        markdown_content: The markdown content to save
        person_name: The name of the person (used for filename)
        output_dir: Directory to save the file (default: networking_agent directory)
    
    Returns:
        Path to the saved file
    """
    if output_dir is None:
        # Save in the networking_agent directory
        output_dir = Path(__file__).parent / "agents" / "networking_agent"
    
    # Sanitize person name for filename
    safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in person_name)
    safe_name = safe_name.replace(' ', '_').lower()
    filename = f"{safe_name}_networking_profile.md"
    
    file_path = output_dir / filename
    
    # Write markdown file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return file_path


def main():
    """Main function to run the networking agent."""
    # Get person name from command line argument or prompt
    if len(sys.argv) > 1:
        person_name = " ".join(sys.argv[1:])
    else:
        person_name = input("Enter the name of the radiologist to research: ").strip()
    
    if not person_name:
        print("Error: Person name is required.")
        sys.exit(1)
    
    print(f"Researching networking profile for: {person_name}")
    print("This may take a few moments...\n")
    
    try:
        # Run the agent
        profile = run_agent(person_name)
        
        # Convert to markdown
        markdown_content = profile_to_markdown(profile)
        
        # Save to file
        file_path = save_markdown_file(markdown_content, person_name)
        
        print(f"\n✓ Successfully created networking profile!")
        print(f"  File saved at: {file_path.absolute()}")
        
    except Exception as e:
        print(f"\n✗ Error running agent: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

