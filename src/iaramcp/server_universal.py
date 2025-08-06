#!/usr/bin/env python3
"""
IaraMCP Universal Server - Supports multiple transport modes
Suporta stdio, http, e sse para compatibilidade com MCP Inspector, Langflow Web e Claude Desktop
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the existing FastMCP instance
from iaramcp.server_claude import mcp


def setup_stdio_mode():
    """Setup for stdio transport mode (Claude Desktop)."""
    print("IaraMCP starting in STDIO mode", file=sys.stderr)
    return mcp


async def setup_http_mode(host: str = "localhost", port: int = 3003):
    """Setup for HTTP transport mode (MCP Inspector, Langflow)."""
    print(f"IaraMCP starting in HTTP mode on {host}:{port}", file=sys.stderr)
    
    # Create HTTP server configuration
    server_config = {
        "host": host,
        "port": port,
        "log_level": "info"
    }
    
    # Return FastMCP with HTTP transport
    return mcp, server_config


async def setup_sse_mode(host: str = "localhost", port: int = 3004):
    """Setup for SSE transport mode."""
    print(f"IaraMCP starting in SSE mode on {host}:{port}", file=sys.stderr)
    
    # Create SSE server configuration
    server_config = {
        "host": host,
        "port": port,
        "log_level": "info"
    }
    
    # Return FastMCP with SSE transport
    return mcp, server_config


def run_stdio():
    """Run server in stdio mode."""
    server = setup_stdio_mode()
    server.run()


async def run_http(host: str = "localhost", port: int = 3003):
    """Run server in HTTP mode."""
    server, config = await setup_http_mode(host, port)
    
    # Run FastMCP with HTTP transport using the correct API
    await server.run_async(
        transport="http",
        host=config["host"],
        port=config["port"]
    )


async def run_sse(host: str = "localhost", port: int = 3004):
    """Run server in SSE mode."""
    server, config = await setup_sse_mode(host, port)
    
    # Run FastMCP with SSE transport using the correct API
    await server.run_async(
        transport="sse",
        host=config["host"],
        port=config["port"]
    )


def main():
    """Main entry point with transport mode selection."""
    parser = argparse.ArgumentParser(description="IaraMCP Universal Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host for HTTP/SSE modes (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3003,
        help="Port for HTTP/SSE modes (default: 3003 for HTTP, 3004 for SSE)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Run in appropriate mode
    if args.transport == "stdio":
        run_stdio()
    elif args.transport == "http":
        asyncio.run(run_http(args.host, args.port))
    elif args.transport == "sse":
        # Use port+1 for SSE if not explicitly set
        sse_port = args.port + 1 if args.port == 3003 else args.port
        asyncio.run(run_sse(args.host, sse_port))


if __name__ == "__main__":
    main()