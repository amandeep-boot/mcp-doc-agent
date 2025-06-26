from typing import Any, Dict, Optional
import httpx
import asyncio
import logging
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from deepwiki.tools import (
    get_repository_details,
    generate_repository_tree,
    get_file_info,
    get_file_content
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("mcp-doc-agent")

# Load the documentation generation prompt
def load_documentation_prompt() -> str:
    """Load the documentation generation prompt from prompt.txt"""
    prompt_file = Path(__file__).parent / "deepwiki" / "prompt" / "prompt.txt"
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"Prompt file not found: {prompt_file}")
        return "You are a documentation generator for software repositories. Please analyze the repository and create comprehensive documentation."

@mcp.prompt()
def documentation_generator() -> str:
    """
    Get the comprehensive documentation generation prompt that explains how to use the available repository analysis tools to create GitBook-ready documentation.
    """
    return load_documentation_prompt()

@mcp.tool()
async def get_repo_details(
    owner: str,
    repo: str
) -> Dict[str, Any]:
    """
    Get detailed information about a GitHub repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
    
    Returns:
        Dictionary containing repository details, README, and root structure
    """
    try:
        logger.info(f"Getting repository details for {owner}/{repo}")
        result = await get_repository_details(owner, repo)
        return result
    except Exception as e:
        logger.error(f"Error getting repository details: {e}")
        return {
            "repo": repo,
            "error": str(e),
            "status": "error"
        }


@mcp.tool()
async def generate_repo_tree(
    owner: str,
    repo: str,
    max_depth: int = 3
) -> Dict[str, Any]:
    """
    Generate a tree structure of the repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        max_depth: Maximum depth to traverse (default: 3, max: 5)
    
    Returns:
        Dictionary containing the repository tree structure
    """
    try:
        # Limit max_depth to prevent too deep traversal
        max_depth = min(max_depth, 5)
        
        logger.info(f"Generating repository tree for {owner}/{repo} with max_depth={max_depth}")
        result = await generate_repository_tree(owner, repo, max_depth)
        return result
    except Exception as e:
        logger.error(f"Error generating repository tree: {e}")
        return {
            "repo": repo,
            "error": str(e),
            "status": "error"
        }


@mcp.tool()
async def get_repo_file_info(
    owner: str,
    repo: str,
    file_path: str
) -> Dict[str, Any]:
    """
    Get information about a specific file (size, type, etc.)
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        file_path: Path to the file in the repository
    
    Returns:
        Dictionary containing file information including size and file type
    """
    try:
        logger.info(f"Getting file info for {owner}/{repo}/{file_path}")
        result = await get_file_info(owner, repo, file_path)
        return result
    except Exception as e:
        logger.error(f"Error getting file info: {e}")
        return {
            "repo": repo,
            "file_path": file_path,
            "error": str(e),
            "status": "error"
        }


@mcp.tool()
async def get_repo_file_content(
    owner: str,
    repo: str,
    file_path: str
) -> Dict[str, Any]:
    """
    Get file content from a GitHub repository
    
    Args:
        owner: Repository owner/organization name
        repo: Repository name
        file_path: Path to the file in the repository
    
    Returns:
        Dictionary containing file content
    """
    try:
        logger.info(f"Getting file content for {owner}/{repo}/{file_path}")
        
        result = await get_file_content(owner, repo, file_path)
        return result
    except Exception as e:
        logger.error(f"Error getting file content: {e}")
        return {
            "repo": repo,
            "file_path": file_path,
            "error": str(e),
            "status": "error"
        }



# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='sse')