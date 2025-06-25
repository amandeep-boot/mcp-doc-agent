"""
GitHub MCP Client for connecting to GitHub MCP Server

This is for Auth
"""

import json
import logging
from typing import Any, Dict
import httpx
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

logger = logging.getLogger(__name__)

# this is for auth
class GitHubMCPClient:
    """GitHub MCP Server client with PAT auth"""
    
    def __init__(self):
        self.github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
        self.mcp_url = "https://api.githubcopilot.com/mcp/"
        
        # check if token is set
        if not self.github_token:
            raise ValueError("Set GITHUB_PERSONAL_ACCESS_TOKEN in .env")
        
        # create client
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.github_token}",
                "Content-Type": "application/json",
                "User-Agent": "mcp-doc-agent/1.0"
            },
            timeout=30.0
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call GitHub MCP server tool"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": f"call-{tool_name}-{id(arguments)}",
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            response = await self.client.post(self.mcp_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            # Handle JSON-RPC 2.0 response format
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            
            # Extract and parse MCP response content
            mcp_result = result.get("result", result)
            return self._parse_mcp_content(mcp_result)
        
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            raise
    
    def _parse_mcp_content(self, mcp_result: Dict[str, Any]) -> Any:
        """Parse MCP content format to extract actual data"""
        if not isinstance(mcp_result, dict):
            return mcp_result
            
        # Handle error responses
        if mcp_result.get("isError"):
            content = mcp_result.get("content", [])
            if content and isinstance(content, list) and len(content) > 0:
                error_msg = content[0].get("text", "Unknown error")
                raise Exception(f"MCP Tool Error: {error_msg}")
            raise Exception("MCP Tool Error: Unknown error")
        
        # Extract content from MCP format
        content = mcp_result.get("content", [])
        if not isinstance(content, list):
            return mcp_result
            
        # If there's only one content item, return its value directly
        if len(content) == 1:
            item = content[0]
            if item.get("type") == "text":
                text = item.get("text", "")
                # Try to parse as JSON if it looks like JSON
                if text.strip().startswith(("[", "{")):
                    try:
                        return json.loads(text)
                    except:
                        return text
                return text
            elif item.get("type") == "resource":
                resource = item.get("resource", {})
                return resource.get("text", resource)
            return item
        
        # Multiple content items - return as list
        parsed_content = []
        for item in content:
            if item.get("type") == "text":
                text = item.get("text", "")
                # Try to parse as JSON if it looks like JSON
                if text.strip().startswith(("[", "{")):
                    try:
                        parsed_content.append(json.loads(text))
                    except:
                        parsed_content.append(text)
                else:
                    parsed_content.append(text)
            elif item.get("type") == "resource":
                resource = item.get("resource", {})
                # Preserve full resource object
                parsed_content.append(resource)
            else:
                parsed_content.append(item)
        
        return parsed_content if len(parsed_content) > 1 else (parsed_content[0] if parsed_content else None) 