"""Custom tools for the article agent.

This module contains custom function tools for searching Semantic Scholar for papers by author name.
"""

import os
import requests

# Get API key if available (optional, but recommended for higher rate limits)
# Environment variables are loaded in main.py
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")


def _format_paper(paper: dict, index: int) -> str:
    """Helper function to format a single paper entry."""
    title = paper.get('title', 'Unknown Title')
    year = paper.get('year', 'Unknown Year')
    venue = paper.get('venue', 'Unknown Venue')
    url = paper.get('url', '')
    citation_count = paper.get('citationCount', 0)
    
    # Format authors
    authors = paper.get('authors', [])
    if authors:
        author_names = [author.get('name', '') for author in authors[:5]]  # Limit to first 5 authors
        authors_str = ', '.join(author_names)
        if len(authors) > 5:
            authors_str += f', et al. ({len(authors)} total authors)'
    else:
        authors_str = 'Unknown Authors'
    
    # Build paper entry
    paper_entry = f"{index}. **{title}**\n"
    paper_entry += f"   - Authors: {authors_str}\n"
    paper_entry += f"   - Journal/Venue: {venue}\n"
    paper_entry += f"   - Year: {year}\n"
    if citation_count > 0:
        paper_entry += f"   - Citations: {citation_count}\n"
    if url:
        paper_entry += f"   - URL: {url}\n"
    
    return paper_entry


def _fetch_papers_from_semantic_scholar(author_name: str, limit: int = 100) -> list:
    """Helper function to fetch papers from Semantic Scholar API."""
    try:
        # Semantic Scholar API endpoint for paper search
        base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        
        # Build query - search for papers by author name
        query = f'author:"{author_name}"'
        
        # Prepare headers
        headers = {}
        if SEMANTIC_SCHOLAR_API_KEY:
            headers["x-api-key"] = SEMANTIC_SCHOLAR_API_KEY
        
        # Parameters for the API request
        params = {
            "query": query,
            "limit": min(limit, 100),  # API limit is 100
            "fields": "title,authors,year,venue,url,citationCount,abstract"
        }
        
        # Make API request
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        papers = data.get('data', [])
        
        return papers
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error accessing Semantic Scholar API: {str(e)}")
    except Exception as e:
        raise Exception(f"Error searching Semantic Scholar: {str(e)}")


def get_semantic_scholar_papers(author_name: str, recent_limit: int, most_cited_limit: int) -> str:
    """Get both recent and most cited papers from Semantic Scholar for an author.
    
    This function searches Semantic Scholar's database for papers authored by the given person
    and returns two lists: the most recent papers and the most cited papers.
    
    Args:
        author_name: The full name of the author to search for (e.g., "John Smith" or "Smith, John")
        recent_limit: Maximum number of recent papers to return (typically 10)
        most_cited_limit: Maximum number of most cited papers to return (typically 10)
    
    Returns:
        A formatted string containing two sections:
        1. Most Recent Papers (up to recent_limit)
        2. Most Cited Papers (up to most_cited_limit)
        
        Each paper includes: Title, Authors, Journal/Venue, Year, URL, Citation Count
        
        Returns an error message if there's an error accessing the API.
    
    Example:
        get_semantic_scholar_papers("Pouria Rouzrokh", 10, 10)
    """
    try:
        # Fetch all papers (we'll need enough to get both recent and most cited)
        max_papers_needed = max(recent_limit, most_cited_limit) * 2  # Get extra to ensure we have enough
        papers = _fetch_papers_from_semantic_scholar(author_name, limit=min(max_papers_needed, 100))
        
        if not papers:
            return f"No papers found for author '{author_name}' in Semantic Scholar database."
        
        # Filter papers with year (for recent sorting)
        papers_with_year = [p for p in papers if p.get('year')]
        
        # Get most recent papers (sorted by year, descending)
        recent_papers = sorted(papers_with_year, key=lambda x: x.get('year', 0) or 0, reverse=True)[:recent_limit]
        
        # Get most cited papers (sorted by citation count, descending)
        # Include papers with citationCount >= 0 (some might be None)
        papers_with_citations = [p for p in papers if p.get('citationCount', 0) is not None]
        most_cited_papers = sorted(
            papers_with_citations, 
            key=lambda x: x.get('citationCount', 0) or 0, 
            reverse=True
        )[:most_cited_limit]
        
        # Remove duplicates (if a paper is both recent and most cited, include it in both lists)
        # But we'll keep them separate as requested
        
        # Format results
        result_parts = []
        
        # Most Recent Papers section
        if recent_papers:
            result_parts.append(f"## Most Recent Papers (up to {recent_limit})\n")
            for i, paper in enumerate(recent_papers, 1):
                result_parts.append(_format_paper(paper, i))
            result_parts.append("")  # Empty line between sections
        else:
            result_parts.append(f"## Most Recent Papers\nNo recent papers found.\n")
        
        # Most Cited Papers section
        if most_cited_papers:
            result_parts.append(f"## Most Cited Papers (up to {most_cited_limit})\n")
            for i, paper in enumerate(most_cited_papers, 1):
                result_parts.append(_format_paper(paper, i))
        else:
            result_parts.append(f"## Most Cited Papers\nNo papers with citations found.\n")
        
        header = f"Papers by '{author_name}' from Semantic Scholar:\n\n"
        return header + '\n'.join(result_parts)
    
    except Exception as e:
        return f"Error: {str(e)}"

