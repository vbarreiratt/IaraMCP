#!/bin/bash
# IaraMCP - Interactive Server Launcher
# Script interativo para selecionar e iniciar o servidor IaraMCP em diferentes modos de transporte

# Set script directory and project paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to display banner
show_banner() {
    echo -e "${CYAN}"
    echo "🧜‍♀️═══════════════════════════════════════════════════════════════🧜‍♀️"
    echo "   IaraMCP - Análise Musical das Águas"
    echo "   Launcher Interativo de Servidor Multi-Transporte"
    echo "🧜‍♀️═══════════════════════════════════════════════════════════════🧜‍♀️"
    echo -e "${NC}"
}

# Function to show transport options
show_transport_options() {
    echo -e "${CYAN}Escolha o modo de transporte:${NC}"
    echo ""
    echo -e "${GREEN}1)${NC} STDIO  ${YELLOW}(Claude Desktop)${NC}"
    echo -e "   Modo padrão para integração com Claude Desktop"
    echo -e "   Usa entrada/saída padrão para comunicação"
    echo ""
    echo -e "${GREEN}2)${NC} HTTP   ${YELLOW}(MCP Inspector, Langflow Web)${NC}"
    echo -e "   Servidor HTTP REST para ferramentas web"
    echo -e "   Padrão: localhost:3003"
    echo ""
    echo -e "${GREEN}3)${NC} SSE    ${YELLOW}(Aplicações Web Avançadas)${NC}"
    echo -e "   Server-Sent Events para aplicações em tempo real"
    echo -e "   Padrão: localhost:3004"
    echo ""
    echo -e "${GREEN}4)${NC} Inspector ${YELLOW}(MCP Inspector para IaraMCP)${NC}"
    echo -e "   Inicia MCP Inspector conectado ao servidor HTTP"
    echo -e "   Automaticamente inicia servidor HTTP se necessário"
    echo ""
    echo -e "${GREEN}5)${NC} Status  ${YELLOW}(Verificar servidores ativos)${NC}"
    echo -e "   Verifica quais servidores estão rodando"
    echo ""
    echo -e "${RED}6)${NC} Sair"
    echo ""
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to show server status
show_status() {
    echo -e "${CYAN}Status dos servidores IaraMCP:${NC}"
    echo ""
    
    # Check STDIO (harder to detect, so we assume it's not running unless we find it)
    echo -e "${YELLOW}STDIO Mode:${NC} Não pode ser detectado automaticamente"
    
    # Check HTTP
    if check_port 3003; then
        echo -e "${YELLOW}HTTP Mode:${NC} ${GREEN}✅ Rodando na porta 3003${NC}"
    else
        echo -e "${YELLOW}HTTP Mode:${NC} ${RED}❌ Não está rodando${NC}"
    fi
    
    # Check SSE  
    if check_port 3004; then
        echo -e "${YELLOW}SSE Mode:${NC} ${GREEN}✅ Rodando na porta 3004${NC}"
    else
        echo -e "${YELLOW}SSE Mode:${NC} ${RED}❌ Não está rodando${NC}"
    fi
    
    # Check Inspector
    if check_port 5174; then
        echo -e "${YELLOW}MCP Inspector:${NC} ${GREEN}✅ Rodando na porta 5174${NC}"
    else
        echo -e "${YELLOW}MCP Inspector:${NC} ${RED}❌ Não está rodando${NC}"
    fi
    
    echo ""
}

# Function to get custom host/port
get_custom_config() {
    local default_host="localhost"
    local default_port=$1
    
    echo -e "${CYAN}Configuração do servidor:${NC}"
    read -p "Host (padrão: $default_host): " host
    host=${host:-$default_host}
    
    read -p "Porta (padrão: $default_port): " port
    port=${port:-$default_port}
    
    echo "$host $port"
}

# Main function
main() {
    show_banner
    
    while true; do
        show_transport_options
        read -p "Selecione uma opção (1-6): " choice
        echo ""
        
        case $choice in
            1)
                echo -e "${BLUE}🧜‍♀️ Iniciando IaraMCP no modo STDIO...${NC}"
                cd "$SCRIPT_DIR"
                ./start_stdio.sh
                ;;
            2)
                echo -e "${BLUE}🧜‍♀️ Iniciando IaraMCP no modo HTTP...${NC}"
                echo -e "${YELLOW}Usar configuração padrão? (y/N)${NC}"
                read -n 1 -r
                echo ""
                
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    cd "$SCRIPT_DIR"
                    ./start_http.sh
                else
                    config=$(get_custom_config 3003)
                    host=$(echo $config | cut -d' ' -f1)
                    port=$(echo $config | cut -d' ' -f2)
                    cd "$SCRIPT_DIR"
                    ./start_http.sh --host "$host" --port "$port"
                fi
                ;;
            3)
                echo -e "${BLUE}🧜‍♀️ Iniciando IaraMCP no modo SSE...${NC}"
                echo -e "${YELLOW}Usar configuração padrão? (y/N)${NC}"
                read -n 1 -r
                echo ""
                
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    cd "$SCRIPT_DIR"
                    ./start_sse.sh
                else
                    config=$(get_custom_config 3004)
                    host=$(echo $config | cut -d' ' -f1)
                    port=$(echo $config | cut -d' ' -f2)
                    cd "$SCRIPT_DIR"
                    ./start_sse.sh --host "$host" --port "$port"
                fi
                ;;
            4)
                echo -e "${BLUE}🔍 Iniciando MCP Inspector para IaraMCP...${NC}"
                cd "$SCRIPT_DIR"
                ./start_inspector.sh
                ;;
            5)
                show_status
                read -p "Pressione Enter para continuar..."
                ;;
            6)
                echo -e "${BLUE}🧜‍♀️ Tchau! A Iara volta para as águas...${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}❌ Opção inválida. Escolha entre 1-6.${NC}"
                echo ""
                ;;
        esac
    done
}

# Run main function
main