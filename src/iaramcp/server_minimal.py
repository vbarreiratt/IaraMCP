#!/usr/bin/env python3
"""
Minimal MCP Server for testing
"""

import asyncio
import sys
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
            description="A simple test tool",
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
            text=f"Test response: {message}"
        )]
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the server."""
    try:
        print("Starting minimal MCP server...", file=sys.stderr)
        async with stdio_server() as (read_stream, write_stream):
            print("Server streams initialized", file=sys.stderr)
            await server.run(
                read_stream, 
                write_stream,
                initialization_options={}
            )
            print("Server running...", file=sys.stderr)
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())