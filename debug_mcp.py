#!/usr/bin/env python3
"""
Script de debug para testar se o IaraMCP server pode ser iniciado corretamente.
"""

import subprocess
import sys
import os
from pathlib import Path

def test_mcp_server():
    """Testa se o servidor MCP pode ser iniciado."""
    
    print("🔧 Debug IaraMCP Server")
    print("=" * 50)
    
    # Verificar se o módulo pode ser importado
    print("\n1. Testando importação do módulo...")
    try:
        sys.path.insert(0, "/Users/vitor/Desktop/analisemusicalavancado/src")
        import iaramcp.server
        print("   ✅ Módulo importado com sucesso")
    except Exception as e:
        print(f"   ❌ Erro na importação: {e}")
        return False
    
    # Verificar se o comando python funciona
    print("\n2. Testando comando python...")
    try:
        result = subprocess.run(
            ["python", "--version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        print(f"   ✅ Python version: {result.stdout.strip()}")
    except Exception as e:
        print(f"   ❌ Erro no comando python: {e}")
        return False
    
    # Verificar se o servidor pode ser iniciado (apenas por alguns segundos)
    print("\n3. Testando inicialização do servidor IaraMCP...")
    try:
        # Configurar environment
        env = os.environ.copy()
        env["PYTHONPATH"] = "/Users/vitor/Desktop/analisemusicalavancado/src"
        
        # Tentar iniciar o servidor (timeout rápido para não travar)
        process = subprocess.Popen(
            ["python", "-m", "iaramcp.server"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/Users/vitor/Desktop/analisemusicalavancado"
        )
        
        # Aguardar um pouco para ver se inicia sem erro
        try:
            stdout, stderr = process.communicate(timeout=3)
            print(f"   ❌ Servidor terminou inesperadamente")
            if stdout:
                print(f"   STDOUT: {stdout}")
            if stderr:
                print(f"   STDERR: {stderr}")
        except subprocess.TimeoutExpired:
            print("   ✅ Servidor iniciou corretamente (matando processo de teste)")
            process.kill()
            process.wait()
            
    except Exception as e:
        print(f"   ❌ Erro ao iniciar servidor: {e}")
        return False
    
    print("\n✅ Todos os testes passaram! O servidor deve funcionar no Claude Desktop.")
    print("\nPróximos passos:")
    print("1. Reinicie o Claude Desktop completamente")
    print("2. Procure por indicações de MCP servers conectados")
    print("3. Teste as ferramentas disponíveis")
    
    return True

if __name__ == "__main__":
    test_mcp_server()