#!/bin/bash
# IaraMCP - MCP Inspector Launcher
# Inicia o MCP Inspector apontando para o servidor IaraMCP

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default values
SERVER_HOST="localhost"
SERVER_PORT=3003
INSPECTOR_PORT=5174

echo -e "${BLUE}🔍 MCP Inspector - IaraMCP${NC}"
echo -e "${YELLOW}   Conectando ao servidor IaraMCP em http://$SERVER_HOST:$SERVER_PORT${NC}"
echo -e "${YELLOW}   Inspector será aberto em http://localhost:$INSPECTOR_PORT${NC}"
echo ""

# Check if MCP Inspector is installed
if ! command -v mcp-inspector &> /dev/null; then
    echo -e "${RED}❌ MCP Inspector não está instalado globalmente${NC}"
    echo -e "${YELLOW}   Instalando MCP Inspector...${NC}"
    npm install -g @modelcontextprotocol/inspector
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Falha na instalação do MCP Inspector${NC}"
        exit 1
    fi
fi

# Check if server is running
if ! curl -s "http://$SERVER_HOST:$SERVER_PORT/health" >/dev/null 2>&1; then
    echo -e "${RED}❌ Servidor IaraMCP não está rodando em http://$SERVER_HOST:$SERVER_PORT${NC}"
    echo -e "${YELLOW}   Inicie o servidor primeiro com:${NC}"
    echo -e "${YELLOW}   ./scripts/start_http.sh${NC}"
    
    # Ask if user wants to start the server
    read -p "Deseja iniciar o servidor automaticamente? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}Iniciando servidor IaraMCP...${NC}"
        # Start server in background
        nohup ./scripts/start_http.sh --host "$SERVER_HOST" --port "$SERVER_PORT" > /tmp/iara_http.log 2>&1 &
        
        # Wait for server to start
        echo -e "${YELLOW}Aguardando servidor iniciar...${NC}"
        for i in {1..30}; do
            if curl -s "http://$SERVER_HOST:$SERVER_PORT/health" >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Servidor iniciado com sucesso!${NC}"
                break
            fi
            sleep 1
        done
        
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ Timeout esperando o servidor iniciar${NC}"
            exit 1
        fi
    else
        exit 1
    fi
fi

# Start MCP Inspector
echo -e "${GREEN}Iniciando MCP Inspector...${NC}"
echo -e "${BLUE}URL do Inspector: http://localhost:6274${NC}"
echo -e "${BLUE}URL do Servidor: http://$SERVER_HOST:$SERVER_PORT${NC}"
echo ""
echo -e "${YELLOW}Pressione Ctrl+C para parar o Inspector${NC}"
echo -e "${YELLOW}O Inspector será aberto automaticamente no navegador${NC}"
echo ""

# Use config file approach for MCP Inspector
CONFIG_FILE="/Users/vitor/Desktop/Encantaria Suite/mcp-inspector-config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ Arquivo de configuração não encontrado: $CONFIG_FILE${NC}"
    echo -e "${YELLOW}   Criando arquivo de configuração...${NC}"
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "matintamcp": {
      "type": "streamable-http",
      "url": "http://localhost:3001"
    },
    "iaramcp": {
      "type": "streamable-http",
      "url": "http://localhost:3003"
    }
  }
}
EOF
fi

mcp-inspector --config "$CONFIG_FILE" --server iaramcp