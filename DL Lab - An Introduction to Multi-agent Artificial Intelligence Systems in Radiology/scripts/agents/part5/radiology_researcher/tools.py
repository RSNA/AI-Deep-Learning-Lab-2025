"""Custom tools for the radiology researcher agent.

This module contains custom function tools that can be used by the agent.
"""

import json
import csv
from pathlib import Path


def create_guidelines_csv(metadata_json: str, filename: str = "radiology_guidelines.csv") -> str:
    """Create a CSV file from JSON metadata about radiology guidelines.
    
    This function takes a JSON string containing metadata about radiology guidelines
    and creates a well-formatted CSV file. The JSON should be an array of objects,
    where each object contains metadata fields like title, website, year, organization, etc.
    
    Args:
        metadata_json: A JSON string containing an array of guideline metadata objects.
                      Each object should have fields like:
                      - title: Title of the guideline
                      - website: URL or domain of the source
                      - year: Publication year
                      - organization: Publishing organization
                      - url: Full URL to the guideline
                      - description: Optional description or summary
        filename: Name of the CSV file to create (default: "radiology_guidelines.csv")
    
    Returns:
        A string message indicating success and the file path where the CSV was saved.
    
    Example JSON input:
        [
            {
                "title": "ACR Appropriateness Criteria for Chest Imaging",
                "website": "acr.org",
                "year": "2023",
                "organization": "American College of Radiology",
                "url": "https://acr.org/...",
                "description": "Guidelines for chest imaging protocols"
            }
        ]
    """
    try:
        # Parse JSON input
        metadata_list = json.loads(metadata_json)
        
        if not isinstance(metadata_list, list):
            return f"Error: Expected a JSON array, but got {type(metadata_list).__name__}"
        
        if len(metadata_list) == 0:
            return "Warning: No metadata provided. CSV file not created."
        
        # Get the directory where this agent file is located
        agent_dir = Path(__file__).parent
        csv_path = agent_dir / filename
        
        # Define CSV columns (extract all unique keys from all objects)
        all_keys = set()
        for item in metadata_list:
            if isinstance(item, dict):
                all_keys.update(item.keys())
        
        # Standardize column order (prefer common fields first)
        preferred_order = ["title", "organization", "year", "website", "url", "description"]
        columns = [col for col in preferred_order if col in all_keys]
        columns.extend(sorted([col for col in all_keys if col not in preferred_order]))
        
        # Write CSV file
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns, extrasaction='ignore')
            writer.writeheader()
            
            for item in metadata_list:
                if isinstance(item, dict):
                    # Clean and format the data
                    cleaned_item = {}
                    for key, value in item.items():
                        # Convert None to empty string, ensure strings are properly encoded
                        if value is None:
                            cleaned_item[key] = ""
                        elif isinstance(value, (list, dict)):
                            cleaned_item[key] = json.dumps(value)
                        else:
                            cleaned_item[key] = str(value)
                    writer.writerow(cleaned_item)
        
        return (
            f"Successfully created CSV file with {len(metadata_list)} guideline(s). "
            f"File saved at: {csv_path.absolute()}"
        )
    
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format. {str(e)}"
    except Exception as e:
        return f"Error creating CSV file: {str(e)}"

