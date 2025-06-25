"""
Repository Details Tool

Get essential information about a GitHub repository including name, readme, and branches count.
"""

from typing import Dict, Any
from .client import GitHubMCPClient


async def get_repository_details(owner: str, repo: str) -> Dict[str, Any]:
    """
    Get essential information about a GitHub repository
    
    Args:
        owner: Repository owner
        repo: Repository name
    
    Returns:
        Dictionary with repository name, readme, branches count, and status
    """
    async with GitHubMCPClient() as client:
        try:
            # Get README content
            readme_content = None
            readme_file = None
            for readme_name in ["README.md", "readme.md", "Readme.md", "README.rst", "README.txt", "README"]:
                try:
                    readme_content = await client.call_tool("get_file_contents", {
                        "owner": owner,
                        "repo": repo,
                        "path": readme_name
                    })
                    readme_file = readme_name
                    break
                except:
                    continue
            
            # Get branches count
            branches_count = 0
            try:
                branches = await client.call_tool("list_branches", {
                    "owner": owner,
                    "repo": repo,
                    "perPage": 100
                })
                branches_count = len(branches) if isinstance(branches, list) else (1 if branches else 0)
            except:
                branches_count = 0
            
            return {
                "repository": f"{owner}/{repo}",
                "readme": {
                    "filename": readme_file,
                    "content": readme_content
                } if readme_content else None,
                "branches_count": branches_count,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "repository": f"{owner}/{repo}",
                "error": str(e),
                "status": "error"
            } 