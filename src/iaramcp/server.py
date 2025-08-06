#!/usr/bin/env python3
"""
MCP Advanced Music Analysis Server

A Model Context Protocol server for advanced audio analysis including
source separation, instrument detection, and comprehensive musical analysis.
"""

import argparse
import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
import traceback

from mcp import server, types as mcp_types
from mcp.server import Server
from mcp.server.models import InitializationOptions

from .audio.analysis import AudioAnalyzer
from .audio.utils import validate_audio_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Server("mcp-advanced-music")

@app.list_tools()
async def handle_list_tools() -> list[mcp_types.Tool]:
    """List available tools for music analysis."""
    return [
        mcp_types.Tool(
            name="analyze_musical_features",
            description="Analyze musical features of an audio file using librosa",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the audio file to analyze"
                    },
                    "analysis_type": {
                        "type": "string",
                        "enum": ["basic", "complete"],
                        "default": "complete",
                        "description": "Type of analysis to perform"
                    }
                },
                "required": ["file_path"]
            }
        ),
        mcp_types.Tool(
            name="validate_audio_file",
            description="Validate if a file is a supported audio format",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the audio file to validate"
                    }
                },
                "required": ["file_path"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[mcp_types.TextContent]:
    """Handle tool calls for music analysis."""
    try:
        if name == "analyze_musical_features":
            return await analyze_musical_features_tool(arguments or {})
        elif name == "validate_audio_file":
            return await validate_audio_file_tool(arguments or {})
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        error_msg = f"Error in {name}: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return [mcp_types.TextContent(type="text", text=error_msg)]

async def analyze_musical_features_tool(arguments: Dict[str, Any]) -> List[mcp_types.TextContent]:
    """Analyze musical features of an audio file."""
    file_path = arguments.get("file_path")
    analysis_type = arguments.get("analysis_type", "complete")
    
    if not file_path:
        raise ValueError("file_path is required")
    
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    # Validate audio file
    validation_result = validate_audio_file(str(file_path))
    if not validation_result["valid"]:
        raise ValueError(f"Invalid audio file: {validation_result['error']}")
    
    # Perform analysis
    analyzer = AudioAnalyzer()
    
    try:
        if analysis_type == "basic":
            result = await analyzer.analyze_basic(str(file_path))
        else:
            result = await analyzer.analyze_complete(str(file_path))
        
        # Format result as JSON
        result_json = json.dumps(result, indent=2, default=str)
        
        return [mcp_types.TextContent(
            type="text", 
            text=f"Musical analysis results for {file_path.name}:\n\n{result_json}"
        )]
        
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")

async def validate_audio_file_tool(arguments: Dict[str, Any]) -> List[mcp_types.TextContent]:
    """Validate an audio file."""
    file_path = arguments.get("file_path")
    
    if not file_path:
        raise ValueError("file_path is required")
    
    result = validate_audio_file(file_path)
    result_json = json.dumps(result, indent=2)
    
    return [mcp_types.TextContent(
        type="text",
        text=f"Audio file validation results:\n\n{result_json}"
    )]

async def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", type=str, default="stdio", help="Transport type (stdio, http, etc.)")
    args = parser.parse_args()

    logger.info("Starting MCP Advanced Music Analysis Server with transport: %s", args.transport)

    if args.transport == "http":
        from mcp.server.http import http_server
        async with http_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-advanced-music",
                    server_version="0.1.0",
                    capabilities=app.get_capabilities()
                )
            )
    else:
        from mcp.server.stdio import stdio_server
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="mcp-advanced-music",
                    server_version="0.1.0",
                    capabilities=app.get_capabilities()
                )
            )

if __name__ == "__main__":
    asyncio.run(main())