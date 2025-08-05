#!/usr/bin/env python3
"""
Teste final do IaraMCP Server - Verifica se tudo está funcionando
"""

import json
import subprocess
import sys
from pathlib import Path

def main():
    print("🎵 TESTE FINAL - IaraMCP Analysis Server")
    print("=" * 55)
    
    # Test 1: Config file validation
    print("\n1. Verificando arquivo de configuração...")
    config_path = Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if 'advanced-music-analysis' in config.get('mcpServers', {}):
            server_config = config['mcpServers']['advanced-music-analysis']
            print(f"   ✅ Configuração encontrada")
            print(f"   Command: {server_config['command']}")
            print(f"   Args: {' '.join(server_config['args'])}")
            print(f"   PYTHONPATH: {server_config['env']['PYTHONPATH']}")
        else:
            print("   ❌ Configuração 'advanced-music-analysis' não encontrada")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao ler configuração: {e}")
        return False
    
    # Test 2: Server startup
    print("\n2. Testando inicialização do servidor...")
    try:
        result = subprocess.run([
            'python', '-c', 
            '''
import asyncio
import subprocess
import sys
import signal

async def test():
    process = subprocess.Popen(
        [sys.executable, "-m", "iaramcp.server_simple"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={"PYTHONPATH": "/Users/vitor/Desktop/analisemusicalavancado/src"}
    )
    
    await asyncio.sleep(1)
    
    if process.poll() is None:
        print("✅ Servidor iniciou com sucesso")
        process.terminate()
        process.wait()
        return True
    else:
        stdout, stderr = process.communicate()
        print("❌ Servidor falhou ao iniciar")
        if stderr:
            print(f"STDERR: {stderr}")
        return False

success = asyncio.run(test())
sys.exit(0 if success else 1)
            '''
        ], cwd="/Users/vitor/Desktop/analisemusicalavancado", capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   " + result.stdout.strip())
        else:
            print("   ❌ Falha na inicialização")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro no teste: {e}")
        return False
    
    # Test 3: Audio file check
    print("\n3. Verificando arquivo de teste...")
    test_file = Path("/Users/vitor/Desktop/NA ONDA DA BABYLON.m4a")
    if test_file.exists():
        size_mb = test_file.stat().st_size / (1024 * 1024)
        print(f"   ✅ Arquivo de teste encontrado: {size_mb:.2f} MB")
    else:
        print(f"   ❌ Arquivo de teste não encontrado: {test_file}")
        return False
    
    print("\n" + "="*55)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Feche completamente o Claude Desktop (Cmd+Q)")
    print("2. Abra o Claude Desktop novamente")
    print("3. Procure por indicação de servidores MCP conectados")
    print("4. Teste com os comandos:")
    print("   • 'Use validate_audio_file com /Users/vitor/Desktop/NA ONDA DA BABYLON.m4a'")
    print("   • 'Use analyze_musical_features para análise completa do arquivo'")
    print("\n💡 DICA: Se não funcionar, verifique os logs em:")
    print("   /Users/vitor/Library/Logs/Claude/main.log")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)