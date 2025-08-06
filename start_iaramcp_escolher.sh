#!/bin/bash

# 🧜‍♀️ Script para escolher o modo de transporte do IaraMCP

echo "🧜‍♀️ IaraMCP - Escolha o Modo de Transporte"
echo "============================================"
echo ""
echo "A Iara pode operar em diferentes modos:"
echo ""
echo "1. 📝 STDIO - Para Claude Desktop"
echo "   ✅ Compatível com Claude Desktop"
echo "   ❌ Não compatível com MCP Inspector"
echo ""
echo "2. 🌐 HTTP - Para MCP Inspector e ferramentas web"
echo "   ❌ Não compatível com Claude Desktop"
echo "   ✅ Compatível com MCP Inspector e outras ferramentas"
echo ""
echo "3. 📡 SSE - Para ferramentas avançadas (Server-Sent Events)"
echo "   ❌ Não compatível com Claude Desktop"
echo "   ✅ Compatível com ferramentas avançadas"
echo ""

read -p "🤔 Escolha o modo (1, 2 ou 3): " choice

cd "/Users/vitor/Desktop/IaraMCP"
export PYTHONPATH="./src"

case $choice in
    1)
        echo ""
        echo "📝 Iniciando em modo STDIO (Claude Desktop)..."
        echo "📋 Configure o Claude Desktop para usar este servidor"
        echo ""
        /opt/anaconda3/bin/python -m iaramcp.server_multi_transport --transport stdio
        ;;
    2)
        echo ""
        echo "🌐 Iniciando em modo HTTP (MCP Inspector)..."
        echo "📡 Servidor estará em: http://localhost:3333"
        echo "📋 Use ./start_inspector_http.sh para conectar o Inspector"
        echo ""
        /opt/anaconda3/bin/python -m iaramcp.server_multi_transport --transport http --port 3333
        ;;
    3)
        echo ""
        echo "📡 Iniciando em modo SSE (Server-Sent Events)..."
        echo "📡 Servidor estará em: http://localhost:3333"
        echo ""
        /opt/anaconda3/bin/python -m iaramcp.server_multi_transport --transport sse --port 3333
        ;;
    *)
        echo "❌ Opção inválida. Escolha 1, 2 ou 3."
        exit 1
        ;;
esac