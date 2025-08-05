#!/usr/bin/env python3
"""
Simplified MCP Advanced Music Analysis Server
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List
import traceback

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types as mcp_types

from .audio.analysis import AudioAnalyzer
from .audio.utils import validate_audio_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the server
server = Server("mcp-advanced-music")

@server.list_prompts()
async def handle_list_prompts() -> list[mcp_types.Prompt]:
    """List available prompts."""
    return []

@server.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """List available tools."""
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

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[mcp_types.TextContent]:
    """Handle tool calls."""
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
    """Run the server."""
    try:
        print("Starting MCP server...", file=sys.stderr)
        async with stdio_server() as streams:
            print("Server streams initialized", file=sys.stderr)
            await server.run(*streams, initialization_options={})
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())