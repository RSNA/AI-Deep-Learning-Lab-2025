"""Custom tools for the biography agent.

This module contains custom function tools that can be used by the agent.
"""

from pathlib import Path
from typing import Optional


def write_biography_markdown(biography_content: str, person_name: str, filename: Optional[str]) -> str:
    """Write a biography to a markdown file.
    
    This function takes biography content and saves it to a markdown file.
    The file will be saved in the same directory as the agent file.
    
    Args:
        biography_content: The biography content in markdown format.
        person_name: The name of the person the biography is about.
        filename: Custom filename (can be None). If None, uses person_name_biography.md
    
    Returns:
        A string message indicating success and the file path where the markdown was saved.
    
    Example:
        write_biography_markdown("# John Doe\n\nJohn Doe was born...", "John Doe")
    """
    try:
        # Get the directory where this agent file is located
        agent_dir = Path(__file__).parent
        
        # Generate filename if not provided
        if filename is None:
            # Sanitize person name for filename
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in person_name)
            safe_name = safe_name.replace(' ', '_').lower()
            filename = f"{safe_name}_biography.md"
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename = f"{filename}.md"
        
        markdown_path = agent_dir / filename
        
        # Write markdown file
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(biography_content)
        
        return (
            f"Successfully created biography markdown file for {person_name}. "
            f"File saved at: {markdown_path.absolute()}"
        )
    
    except Exception as e:
        return f"Error creating markdown file: {str(e)}"

