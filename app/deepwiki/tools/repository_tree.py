"""
Repository Tree Tool

Generate a tree structure of a GitHub repository with configurable depth.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from .client import GitHubMCPClient


async def generate_repository_tree(owner: str, repo: str, max_depth: int = 3) -> Dict[str, Any]:
    """
    Generate a tree structure of the repository
    
    Args:
        owner: Repository owner
        repo: Repository name
        max_depth: Maximum depth to traverse (default: 3)
    
    Returns:
        Dictionary with tree structure
    """
    async def build_tree(client: GitHubMCPClient, path: str = "", current_depth: int = 0) -> Dict[str, Any]:
        """Recursively build tree structure"""
        if current_depth >= max_depth:
            return {"truncated": True, "reason": "max_depth_reached"}
        
        try:
            # For directories, path must end with "/"
            if path == "":
                # Root directory
                actual_path = "/"
            else:
                # check paths end with "/"
                actual_path = path if path.endswith("/") else f"{path}/"
            
            args = {
                "owner": owner,
                "repo": repo,
                "path": actual_path
            }
                
            contents = await client.call_tool("get_file_contents", args)
            
            if not isinstance(contents, list):
                # It's a file, not a directory
                return {
                    "type": "file",
                    "name": contents.get("name", Path(path).name if path else "root") if isinstance(contents, dict) else (Path(path).name if path else "root"),
                    "path": path,
                    "size": contents.get("size", 0) if isinstance(contents, dict) else 0
                }
            
            # It's a directory
            tree = {
                "type": "directory",
                "name": Path(path).name if path else "root",
                "path": path,
                "children": []
            }
            
            try:
                # Sort contents: directories first, then files
                directories = [item for item in contents if isinstance(item, dict) and item.get("type") == "dir"]
                files = [item for item in contents if isinstance(item, dict) and item.get("type") == "file"]
                
                # Add directories first
                for item in directories:
                    try:
                        item_path = item.get("path", "")
                        child_tree = await build_tree(client, item_path, current_depth + 1)
                        tree["children"].append(child_tree)
                    except Exception as e:
                        # Add error direcs 
                        tree["children"].append({
                            "type": "error",
                            "name": item.get("name", "unknown"),
                            "path": item.get("path", ""),
                            "error": str(e)
                        })
                
                # Add files
                for item in files:
                    tree["children"].append({
                        "type": "file",
                        "name": item.get("name", ""),
                        "path": item.get("path", ""),
                        "size": item.get("size", 0)
                    })
            except Exception as e:
                # If we can't process children, at least return the directory info
                tree["error"] = f"Error processing children: {str(e)}"
            
            return tree
            
        except Exception as e:
            return {
                "type": "error",
                "name": Path(path).name if path else "root",
                "path": path,
                "error": str(e)
            }
    
    # Main function body
    try:
        async with GitHubMCPClient() as client:
            tree = await build_tree(client)
            return {
                "repository": f"{owner}/{repo}",
                "max_depth": max_depth,
                "tree": tree,
                "status": "success"
            }
    except Exception as e:
        return {
            "repository": f"{owner}/{repo}",
            "max_depth": max_depth,
            "error": str(e),
            "status": "error"
        } 