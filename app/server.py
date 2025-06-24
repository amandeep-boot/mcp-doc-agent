from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP



mcp = FastMCP("mcp-doc-agent")



@mcp.tool()
async def get_documentation():
    return "MCP-server is running with FastMCP."


# if __name__ == "__main__":
#     # Initialize and run the server
#     mcp.run(transport='sse')