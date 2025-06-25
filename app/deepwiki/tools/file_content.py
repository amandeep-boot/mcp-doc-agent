"""
File Content Tool

Get the content of a specific file in a GitHub repository
"""

from typing import Dict, Any, Optional
import base64
from .client import GitHubMCPClient


async def get_file_content(
    owner: str, 
    repo: str, 
    file_path: str
) -> Dict[str, Any]:
    """
    Get file content from a GitHub repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        file_path: Path to the file
    
    Returns:
        Dictionary with file content and metadata
    """
    async with GitHubMCPClient() as client:
        try:
            args = {
                "owner": owner,
                "repo": repo,
                "path": file_path
            }
            
            file_data = await client.call_tool("get_file_contents", args)
            
            # Extract content - handle MCP resource format from GitHub MCP server
            content = ""
            if isinstance(file_data, dict):
                # Check for MCP resource format (from GitHub MCP server)
                if "text" in file_data:
                    content = file_data["text"]
                elif "blob" in file_data:
                    # Handle base64 blob content
                    try:
                        content = base64.b64decode(file_data["blob"]).decode('utf-8')
                    except Exception as e:
                        return {
                            "repo": repo,
                            "file_path": file_path,
                            "error": f"Could not decode blob content: {str(e)}",
                            "status": "error"
                        }
                elif "content" in file_data:
                    # Handle base64 encoded content
                    try:
                        content = base64.b64decode(file_data["content"]).decode('utf-8')
                    except Exception as e:
                        return {
                            "repo": repo,
                            "file_path": file_path,
                            "error": f"Could not decode file content: {str(e)}",
                            "status": "error"
                        }
                else:
                    # Fallback: convert entire response to string
                    content = str(file_data)
            elif isinstance(file_data, str):
                content = file_data
            else:
                content = str(file_data)
            
            return {
                "repo": repo,
                "file_path": file_path,
                "content": content,
                "size": len(content),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "repo": repo,
                "file_path": file_path,
                "error": str(e),
                "status": "error"
            } 