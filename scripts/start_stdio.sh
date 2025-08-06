#!/bin/bash
# IaraMCP - Starter Script STDIO Mode
# Inicia o servidor IaraMCP no modo STDIO para Claude Desktop

# Set script directory and project paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_DIR/src"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧜‍♀️ IaraMCP - Iniciando no modo STDIO${NC}"
echo -e "${YELLOW}   Para uso com Claude Desktop${NC}"
echo ""

# Set environment variables
export PYTHONPATH="$SRC_DIR"
export IARAMCP_VIS_MODE="local"
export IARAMCP_TEMP_DIR="$HOME/Desktop/IaraMCP_Output"
export IARAMCP_LOG_LEVEL="INFO"
export IARAMCP_INTEGRATION_MODE="full"

# Create output directory if it doesn't exist
mkdir -p "$HOME/Desktop/IaraMCP_Output"

# Start server in stdio mode
echo -e "${GREEN}Executando: python -m iaramcp.server_universal --transport stdio${NC}"
cd "$PROJECT_DIR"
python -m iaramcp.server_universal --transport stdio