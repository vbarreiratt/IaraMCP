# 🧜‍♀️ AGENTE.md - Manual Técnico IaraMCP

*Guia completo para desenvolvedores e agentes trabalhando com o servidor IaraMCP*

## 🏗️ Arquitetura do Sistema

### Estrutura Modular
```
IaraMCP/
├── src/iaramcp/
│   ├── server_fastmcp.py      # 🎯 Servidor principal (ponto de entrada)
│   ├── audio/                 # 📊 Módulo de processamento de áudio
│   │   ├── analysis.py        # Análise musical (librosa)
│   │   ├── separation.py      # Separação de fontes (Demucs) 
│   │   └── utils.py          # Utilitários de validação
│   ├── ml/                   # 🤖 Machine Learning
│   │   └── classifier.py     # Classificação de instrumentos
│   ├── visualization/        # 📈 Visualizações
│   │   └── plots.py          # Geração de gráficos
│   └── optimization/         # ⚡ Performance
│       └── performance.py    # Cache e otimizações
└── requirements*.txt         # Dependências
```

### Ponto de Entrada Principal
**Arquivo**: `src/iaramcp/server_fastmcp.py`
- **FastAPI app**: Roda na porta 3333, endpoint `/` para health check
- **FastMCP app**: Montado em `/mcp`, contém todas as 22 ferramentas
- **Arquitetura híbrida**: Permite deployment tanto como MCP server quanto API web

## 🛠️ Sistema de Ferramentas

### Convenção de Nomenclatura
Todas as ferramentas seguem o padrão temático da Iara:
- `iara_[verbo]_[substantivo_tematico]`
- Exemplo: `iara_mergulhar_nas_ondas` = análise musical
- Nomes em português para manter a temática brasileira

### Categorias de Ferramentas

#### 1. Análise e Validação (5 ferramentas)
```python
@mcp.tool()
def iara_despertar(mensagem: str = "Olá") -> str
@mcp.tool()
async def iara_mergulhar_nas_ondas(caminho_arquivo: str, tipo_analise: str = "completa") -> dict
@mcp.tool()
def iara_validar_cristais_sonoros(caminho_arquivo: str) -> dict
@mcp.tool()
async def iara_tecer_relatorio_das_aguas(file_path: str, format: str = "json") -> dict
@mcp.tool()
def iara_explorar_caverna_sonora(directory_path: str, file_extensions: List[str]) -> dict
```

#### 2. Separação de Fontes (4 ferramentas)
```python
@mcp.tool()
async def iara_separar_correntes_musicais(caminho_arquivo: str, modelo: str = "htdemucs_ft") -> dict
@mcp.tool()
async def iara_examinar_corrente_isolada(stem_path: str, instrument_type: str = "auto") -> dict
@mcp.tool()
async def iara_comparar_magias_separadoras(file_path: str, methods: List[str]) -> dict
@mcp.tool()
def iara_revelar_segredos_separacao() -> dict
```

#### 3. Classificação de Instrumentos (4 ferramentas)
```python
@mcp.tool()
async def iara_reconhecer_instrumentos_das_aguas(caminho_arquivo: str, limiar_confianca: float = 0.7) -> dict
@mcp.tool()
async def iara_identificar_voz_das_aguas(stem_path: str, expected_type: str = "auto") -> dict
@mcp.tool()
async def iara_revelar_alma_do_instrumento(file_path: str, instrument_type: str) -> dict
@mcp.tool()
def iara_mostrar_sabedoria_classificadora() -> dict
```

#### 4. Visualizações (5 ferramentas)
```python
@mcp.tool()
async def iara_visualizar_ondas_do_tempo(caminho_arquivo: str, caminho_saida: str = None) -> dict
@mcp.tool()
async def iara_criar_mapa_das_frequencias(caminho_arquivo: str, tipo_espectrograma: str = "stft") -> dict
@mcp.tool()
async def iara_pintar_essencia_musical(file_path: str, plot_type: str = "comprehensive") -> dict
@mcp.tool()
async def iara_desenhar_correntes_separadas(file_path: str, separation_method: str = "htdemucs_ft") -> dict
@mcp.tool()
def iara_revelar_artes_visuais() -> dict
```

#### 5. Otimização (4 ferramentas)
```python
@mcp.tool()
def iara_mostrar_poder_das_aguas() -> dict
@mcp.tool()
def iara_purificar_memorias() -> dict
@mcp.tool()
async def iara_harmonizar_fluxo_musical(file_path: str, operations: list = None) -> dict
@mcp.tool()
def iara_compartilhar_sabedoria_otimizacao() -> dict
```

## 🔧 Sistema de Fallback Cross-Platform

### Detecção de Ambiente
```python
def detectar_modo_visualizacao() -> str:
    """
    Detecta se está rodando local (Claude Desktop) ou remoto (Smithery.ai)
    - Local: Salva arquivos no filesystem  
    - Remoto: Retorna base64/dados em memória
    """
    if os.environ.get("IARAMCP_VIS_MODE") == "local":
        return "local"
    if os.environ.get("DISPLAY") or sys.platform in ("darwin", "win32"):
        return "local"
    return "web"
```

### Sistema de Paths Dinâmicos
```python
def definir_caminho_saida(nome_base: str, extensao: str = ".png") -> Optional[str]:
    """
    Define path de saída baseado no ambiente:
    - Local: /Users/vitor/Desktop/{nome_base}{extensao}
    - Remoto: None (força base64)
    """
    if MODO_VISUALIZACAO == "local":
        return os.path.join("/Users/vitor/Desktop", f"{nome_base}{extensao}")
    return None
```

## 📦 Gerenciamento de Dependências

### Dependências Obrigatórias
```python
# Core MCP
mcp>=1.0.0
fastmcp>=0.2.0

# Audio processing básico  
librosa>=0.10.0
numpy>=1.21.0
scipy>=1.7.0
soundfile>=0.12.0
```

### Dependências Avançadas (Opcionais)
```python
# Source separation
demucs>=4.0.0
torch>=2.0.0
torchaudio>=2.0.0

# ML & Visualization
scikit-learn>=1.0.0
matplotlib>=3.5.0

# Removed for Docker compatibility:
# essentia>=2.1b6.dev858  # Complex build
# madmom>=0.16.1          # Complex dependencies
```

### Sistema de Fallback para Imports
```python
try:
    from iaramcp.audio.analysis import AudioAnalyzer
    AUDIO_ANALYSIS_AVAILABLE = True
except ImportError:
    # Cria classes dummy que retornam erros informativos
    class AudioAnalyzer:
        async def analyze_basic(self, file_path):
            return {"error": "Audio analysis not available - missing dependencies"}
    AUDIO_ANALYSIS_AVAILABLE = False
```

## 🚀 Setup de Desenvolvimento

### Ambiente Local
```bash
# 1. Clone o repositório
git clone <repo-url>
cd IaraMCP

# 2. Setup Python virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -e .[advanced]

# 4. Test server
PYTHONPATH=./src python -m iaramcp.server_fastmcp

# 5. Test with MCP Inspector  
npx @modelcontextprotocol/inspector python -m iaramcp.server_fastmcp
```

### Variáveis de Ambiente
```bash
# Força modo local (desenvolvimento)
export IARAMCP_VIS_MODE=local

# Python path para desenvolvimento
export PYTHONPATH="/caminho/para/IaraMCP/src"
```

### Comandos de Desenvolvimento Úteis
```bash
# Test import e tools
PYTHONPATH=./src python -c "
import iaramcp.server_fastmcp as server
print('Ferramentas:', [attr for attr in dir(server) if attr.startswith('iara_')])
"

# Start server manualmente
PYTHONPATH=./src python -m iaramcp.server_fastmcp

# Verificar dependências
pip show demucs torch librosa
```

## 🔍 Debugging e Troubleshooting

### Problemas Comuns

#### 1. Import Errors
```python
# Sintoma: ImportError para librosa/demucs
# Solução: Sistema de fallback ativo, ferramentas retornam errors informativos
# Debug: Verificar AUDIO_ANALYSIS_AVAILABLE, SOURCE_SEPARATION_AVAILABLE flags
```

#### 2. Path Issues  
```python
# Sintoma: Arquivos não encontrados
# Solução: Verificar PYTHONPATH e caminhos absolutos
# Debug: print(sys.path), os.getcwd()
```

#### 3. Visualização não funcionando
```python
# Sintoma: Gráficos não aparecem
# Solução: Verificar detectar_modo_visualizacao(), ajustar paths
# Debug: Testar com IARAMCP_VIS_MODE=local
```

### Logs e Debugging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Adicionar logs nas ferramentas para debug
logger.info(f"Processing file: {file_path}")
logger.debug(f"Detection mode: {detectar_modo_visualizacao()}")
```

## 🏭 Deployment e Produção

### Claude Desktop Configuration
```json
{
  "mcpServers": {
    "iaramcp": {
      "command": "python",
      "args": ["-m", "iaramcp.server_fastmcp"],
      "env": {
        "PYTHONPATH": "/caminho/completo/para/IaraMCP/src"
      }
    }
  }
}
```

### Docker Deployment (Smithery.ai)
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg
COPY requirements-docker.txt .
RUN pip install -r requirements-docker.txt
COPY src/ /app/src/
WORKDIR /app
EXPOSE 3333
CMD ["python", "-m", "iaramcp.server_fastmcp"]
```

### Performance Considerations
- **Cache**: Sistema LRU cache para análises repetidas
- **Memória**: Fallback para chunks em arquivos grandes  
- **CPU**: Processamento paralelo quando possível
- **I/O**: Otimização de leitura/escrita de arquivos

## 🧪 Testing

### Unit Tests Structure
```python
# test_tools.py
import pytest
from iaramcp.server_fastmcp import iara_despertar

def test_despertar():
    result = iara_despertar("teste")
    assert "IaraMCP está despertando" in result

async def test_analysis():
    # Mock file path para teste
    result = await iara_mergulhar_nas_ondas("test_file.mp3", "basica")
    assert "erro" in result or "analysis" in result
```

### Integration Tests
```python
# test_integration.py  
def test_full_workflow():
    # Test complete workflow com arquivo real
    # 1. Validar arquivo
    # 2. Análise básica  
    # 3. Verificar outputs
```

## 📊 Monitoramento e Métricas

### Performance Metrics
```python
def get_performance_stats():
    return {
        "cache_hits": optimizer.cache_hits,
        "processing_times": optimizer.avg_times,
        "memory_usage": get_memory_usage(),
        "tools_usage": get_tools_usage_stats()
    }
```

### Health Checks
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "modules": {
            "analysis": AUDIO_ANALYSIS_AVAILABLE,
            "separation": SOURCE_SEPARATION_AVAILABLE,
            "visualization": VISUALIZATION_AVAILABLE
        }
    }
```

## 🔒 Segurança e Validação

### Input Validation
```python
def validate_audio_file(file_path: str) -> dict:
    """
    Valida arquivos de entrada:
    - Existência do arquivo
    - Formato suportado
    - Tamanho razoável
    - Não executável
    """
    if not Path(file_path).exists():
        return {"valid": False, "error": "File not found"}
    
    # Check file extension
    valid_extensions = ['.mp3', '.wav', '.flac', '.m4a', '.ogg']
    if not any(file_path.lower().endswith(ext) for ext in valid_extensions):
        return {"valid": False, "error": "Unsupported format"}
    
    return {"valid": True}
```

### Error Handling
```python
try:
    result = await some_analysis_function(file_path)
    return result
except Exception as e:
    import traceback
    return {
        "erro": f"Analysis failed: {str(e)}",
        "traceback": traceback.format_exc()
    }
```

## 🔮 Extensibilidade

### Adicionando Nova Ferramenta
```python
@mcp.tool()
async def iara_nova_funcionalidade(parametro: str) -> dict:
    """
    Nova funcionalidade da Iara - Descrição detalhada
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        Resultado da operação
    """
    try:
        # Implementação
        return {"resultado": "sucesso"}
    except Exception as e:
        return {"erro": str(e)}
```

### Integrando Novo Módulo
1. Criar módulo em `src/iaramcp/novo_modulo/`
2. Adicionar import com fallback em `server_fastmcp.py`
3. Registrar ferramentas com decorador `@mcp.tool()`
4. Atualizar documentação

---

🧜‍♀️ *Este manual técnico garante que desenvolvedores e agentes possam trabalhar eficientemente com o IaraMCP, mantendo a qualidade e a temática brasileira do projeto.*