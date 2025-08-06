#!/bin/bash

# 🧜‍♀️ Script para iniciar IaraMCP em modo HTTP (para Inspector)

echo "🧜‍♀️ Iniciando IaraMCP - Servidor HTTP da Iara..."
echo "================================================"

# Ir para o diretório correto
cd "/Users/vitor/Desktop/IaraMCP"

# Definir PYTHONPATH
export PYTHONPATH="./src"

# Mostrar informações
echo "📁 Diretório: $(pwd)"
echo "🐍 Python: /opt/anaconda3/bin/python"
echo "🔧 PYTHONPATH: $PYTHONPATH"
echo "🌐 Modo: HTTP"
echo "📡 URL: http://localhost:3333"
echo ""

# Verificar se tudo está OK
echo "🔍 Verificando dependências..."
/opt/anaconda3/bin/python -c "
try:
    import iaramcp.server_multi_transport
    print('✅ IaraMCP está pronto!')
except Exception as e:
    print(f'❌ Erro: {e}')
    exit(1)
"

echo ""
echo "🌊 Iniciando servidor da Iara em modo HTTP..."
echo "⚠️  Para parar o servidor, pressione Ctrl+C"
echo "📝 Este modo é compatível com MCP Inspector"
echo "🌐 Servidor estará em: http://localhost:3333"
echo ""

# Iniciar o servidor em modo HTTP
/opt/anaconda3/bin/python -m iaramcp.server_multi_transport --transport http --port 3333