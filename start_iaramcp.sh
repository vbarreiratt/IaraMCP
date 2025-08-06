#!/bin/bash

# 🧜‍♀️ Script de inicialização do IaraMCP

echo "🧜‍♀️ Iniciando IaraMCP - Servidor da Iara Musical..."
echo "=================================================="

# Ir para o diretório correto
cd "/Users/vitor/Desktop/IaraMCP"

# Definir PYTHONPATH
export PYTHONPATH="./src"

# Mostrar informações
echo "📁 Diretório: $(pwd)"
echo "🐍 Python: /opt/anaconda3/bin/python"
echo "🔧 PYTHONPATH: $PYTHONPATH"
echo ""

# Verificar se tudo está OK
echo "🔍 Verificando dependências..."
/opt/anaconda3/bin/python -c "
try:
    import iaramcp.server_fastmcp
    print('✅ IaraMCP está pronto!')
except Exception as e:
    print(f'❌ Erro: {e}')
    exit(1)
"

echo ""
echo "🌊 Iniciando servidor da Iara..."
echo "⚠️  Para parar o servidor, pressione Ctrl+C"
echo "📝 Deixe este terminal aberto enquanto usar o IaraMCP"
echo ""

# Iniciar o servidor em modo STDIO (Claude Desktop)
/opt/anaconda3/bin/python -m iaramcp.server_multi_transport --transport stdio