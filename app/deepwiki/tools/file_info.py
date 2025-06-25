"""
File Information Tool

Get detailed information about a specific file in a GitHub repository.
"""

from typing import Dict, Any, Optional
from .client import GitHubMCPClient


async def get_file_info(owner: str, repo: str, file_path: str) -> Dict[str, Any]:
    """
    Get information about a specific file in a repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        file_path: Path to the file
    
    Returns:
        Dictionary with file information
    """
    async with GitHubMCPClient() as client:
        try:
            args = {
                "owner": owner,
                "repo": repo,
                "path": file_path
            }
            
            file_data = await client.call_tool("get_file_contents", args)
            
            return {
                "repo": repo,
                "file_path": file_path,
                "name": file_data.get("name", file_path.split("/")[-1]) if isinstance(file_data, dict) else file_path.split("/")[-1],
                "size": file_data.get("size", 0) if isinstance(file_data, dict) else len(str(file_data)),
                "type": file_data.get("type", "file") if isinstance(file_data, dict) else "file",
                "status": "success"
            }
            
        except Exception as e:
            return {
                "repo": repo,
                "file_path": file_path,
                "error": str(e),
                "status": "error"
            } 