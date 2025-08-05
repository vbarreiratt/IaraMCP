#!/usr/bin/env python3
"""
Fixed MCP Advanced Music Analysis Server
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types as mcp_types

# Create the server
server = Server("mcp-advanced-music")

@server.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """List available tools."""
    return [
        mcp_types.Tool(
            name="test_tool",
            description="A simple test tool for music analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Test message"
                    }
                },
                "required": ["message"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[mcp_types.TextContent]:
    """Handle tool calls."""
    if name == "test_tool":
        message = arguments.get("message", "Hello")
        return [mcp_types.TextContent(
            type="text",
            text=f"Music analysis test response: {message}"
        )]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream,
            # Remove initialization_options parameter that's causing issues
        )

if __name__ == "__main__":
    asyncio.run(main())