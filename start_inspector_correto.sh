#!/bin/bash

# 🔍 MCP Inspector - Sintaxe Correta

echo "🔍 MCP Inspector - IaraMCP"
echo "========================="
echo ""

cd /Users/vitor/Desktop/IaraMCP

# Criar arquivo de configuração no formato correto (somente conexão via URL)
cat > inspector_config.json << EOF
{
  "mcpServers": {
    "iaramcp": {
      "url": "http://localhost:3333"
    }
  }
}
EOF

echo "✅ Configuração criada: inspector_config.json"
echo ""
echo "🌊 Iniciando Inspector da Iara..."
echo "⚠️  Para parar, pressione Ctrl+C"
echo "🌐 URL: http://localhost:5173"
echo ""

# Iniciar o inspector apenas como cliente
npx @modelcontextprotocol/inspector --config inspector_config.json --server iaramcp --no-open