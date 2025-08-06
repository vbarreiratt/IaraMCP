#!/bin/bash
# IaraMCP - Starter Script HTTP Mode
# Inicia o servidor IaraMCP no modo HTTP para MCP Inspector e Langflow

# Set script directory and project paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_DIR/src"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
HOST="localhost"
PORT=3003

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --host)
      HOST="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --help)
      echo "Uso: $0 [--host HOST] [--port PORT]"
      echo "  --host: Host para servidor HTTP (padrão: localhost)"
      echo "  --port: Porta para servidor HTTP (padrão: 3003)"
      exit 0
      ;;
    *)
      echo -e "${RED}Opção desconhecida: $1${NC}"
      echo "Use --help para ver as opções disponíveis"
      exit 1
      ;;
  esac
done

echo -e "${BLUE}🧜‍♀️ IaraMCP - Iniciando no modo HTTP${NC}"
echo -e "${YELLOW}   Para uso com MCP Inspector e Langflow Web${NC}"
echo -e "${YELLOW}   Servidor será iniciado em: http://$HOST:$PORT${NC}"
echo ""

# Set environment variables
export PYTHONPATH="$SRC_DIR"
export IARAMCP_VIS_MODE="local"
export IARAMCP_TEMP_DIR="$HOME/Desktop/IaraMCP_Output"
export IARAMCP_LOG_LEVEL="INFO"
export IARAMCP_INTEGRATION_MODE="full"

# Create output directory if it doesn't exist
mkdir -p "$HOME/Desktop/IaraMCP_Output"

# Check if port is available
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}❌ Porta $PORT já está em uso!${NC}"
    echo -e "${YELLOW}   Use outro porto: $0 --port NOVA_PORTA${NC}"
    exit 1
fi

# Start server in HTTP mode
echo -e "${GREEN}Executando: python -m iaramcp.server_universal --transport http --host $HOST --port $PORT${NC}"
cd "$PROJECT_DIR"
python -m iaramcp.server_universal --transport http --host "$HOST" --port "$PORT"