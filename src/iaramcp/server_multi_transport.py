#!/usr/bin/env python3
"""
IaraMCP - Servidor Multi-Transporte
Suporta stdio (Claude Desktop), http e sse (Inspector/outras ferramentas)
"""

import sys
import argparse
from pathlib import Path

# Importar o servidor FastMCP existente
from iaramcp.server_fastmcp import mcp

def main():
    parser = argparse.ArgumentParser(description="IaraMCP - Servidor Multi-Transporte da Iara")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http", "sse"], 
        default="stdio",
        help="Protocolo de transporte: stdio (Claude Desktop), http (Inspector), sse (Server-Sent Events)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=3333,
        help="Porta para HTTP/SSE (padrão: 3333)"
    )
    parser.add_argument(
        "--host", 
        default="localhost",
        help="Host para HTTP/SSE (padrão: localhost)"
    )
    
    args = parser.parse_args()
    
    print(f"🧜‍♀️ IaraMCP - Iniciando servidor da Iara")
    print(f"🌊 Transporte: {args.transport.upper()}")
    
    if args.transport == "stdio":
        print("📝 Modo STDIO - Compatível com Claude Desktop")
        print("📋 Configure o Claude Desktop para usar este servidor")
        mcp.run(transport="stdio")
    
    elif args.transport == "http":
        print(f"🌐 Modo HTTP - Servidor em http://{args.host}:{args.port}")
        print("📋 Compatível com MCP Inspector e outras ferramentas HTTP")
        mcp.run(transport="http", host=args.host, port=args.port)
    
    elif args.transport == "sse":
        print(f"📡 Modo SSE - Servidor em http://{args.host}:{args.port}")
        print("📋 Compatível com ferramentas que usam Server-Sent Events")
        mcp.run(transport="sse", host=args.host, port=args.port)

if __name__ == "__main__":
    main()