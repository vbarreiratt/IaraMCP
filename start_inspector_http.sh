#!/bin/bash

# 🔍 MCP Inspector - Conecta via HTTP ao servidor IaraMCP

echo "🔍 MCP Inspector - Conexão HTTP"
echo "================================"
echo ""
echo "📝 IMPORTANTE: Certifique-se de que o servidor HTTP está rodando!"
echo "   Execute em outro terminal: ./start_iaramcp_http.sh"
echo ""

cd /Users/vitor/Desktop/IaraMCP

# Verificar se o servidor está rodando
echo "🔍 Verificando se o servidor está rodando em http://localhost:3333..."
if curl -s http://localhost:3333/health > /dev/null 2>&1; then
    echo "✅ Servidor encontrado!"
else
    echo "❌ Servidor não encontrado em http://localhost:3333"
    echo ""
    echo "📋 Para resolver:"
    echo "1. Abra outro terminal"
    echo "2. Execute: cd /Users/vitor/Desktop/IaraMCP"
    echo "3. Execute: ./start_iaramcp_http.sh"
    echo "4. Aguarde o servidor iniciar completamente"
    echo "5. Volte aqui e execute este script novamente"
    echo ""
    read -p "Pressione Enter quando o servidor estiver rodando..."
fi

# Criar arquivo de configuração para conexão HTTP
cat > inspector_config_http.json << EOF
{
  "mcpServers": {
    "iaramcp": {
      "url": "http://localhost:3333"
    }
  }
}
EOF

echo ""
echo "✅ Configuração HTTP criada: inspector_config_http.json"
echo ""
echo "🌊 Conectando Inspector ao servidor HTTP da Iara..."
echo "⚠️  Para parar, pressione Ctrl+C"
echo "🌐 Interface do Inspector: http://localhost:5173"
echo ""

# Iniciar o inspector conectando via HTTP
npx @modelcontextprotocol/inspector --config inspector_config_http.json --server iaramcp