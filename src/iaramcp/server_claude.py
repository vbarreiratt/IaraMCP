#!/usr/bin/env python3
"""
IaraMCP - Servidor para Claude Desktop
Versão específica para Claude Desktop usando apenas FastMCP
"""

from fastmcp import FastMCP
from pathlib import Path
import json
import sys
import os
import asyncio
import time
import logging
from typing import Dict, List, Optional, Any

# Função para detectar o modo de visualização
def detectar_modo_visualizacao() -> str:
    """Detecta o modo de visualização do ambiente."""
    if os.environ.get("IARAMCP_VIS_MODE") == "local":
        return "local"
    if os.environ.get("DISPLAY") or sys.platform in ("darwin", "win32"):
        return "local"
    return "web"

MODO_VISUALIZACAO = detectar_modo_visualizacao()

def definir_caminho_saida(nome_base: str, extensao: str = ".png") -> Optional[str]:
    if MODO_VISUALIZACAO == "local":
        return os.path.join("/Users/vitor/Desktop", f"{nome_base}{extensao}")
    else:
        return None

logger = logging.getLogger(__name__)

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Try to import modules with fallback
try:
    from iaramcp.audio.analysis import AudioAnalyzer
    from iaramcp.audio.utils import validate_audio_file, get_audio_info
    from iaramcp.audio.separation import SourceSeparator
    from iaramcp.ml.classifier import InstrumentClassifier
    from iaramcp.visualization.plots import AudioVisualizer
    from iaramcp.optimization.performance import PerformanceOptimizer
    AUDIO_ANALYSIS_AVAILABLE = True
    SOURCE_SEPARATION_AVAILABLE = True
    INSTRUMENT_CLASSIFICATION_AVAILABLE = True
    VISUALIZATION_AVAILABLE = True
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    # Fallback classes with error messages
    def validate_audio_file(file_path):
        return {"valid": True, "format": "unknown", "duration": 0}
    
    def get_audio_info(file_path):
        return {"file": file_path, "error": "Audio analysis not available"}
    
    class AudioAnalyzer:
        async def analyze_basic(self, file_path):
            return {"error": "Audio analysis not available - missing dependencies"}
        async def analyze_complete(self, file_path):
            return {"error": "Audio analysis not available - missing dependencies"}
    
    class SourceSeparator:
        def __init__(self, model_name='htdemucs_ft', device='auto'):
            pass
        async def separate_audio(self, file_path, **kwargs):
            return {"error": "Source separation not available - missing dependencies"}
    
    class InstrumentClassifier:
        async def identify_instruments(self, file_path, **kwargs):
            return {"error": "Instrument classification not available - missing dependencies"}
    
    class AudioVisualizer:
        async def create_waveform(self, file_path, **kwargs):
            return {"error": "Visualization not available - missing dependencies"}
    
    class PerformanceOptimizer:
        def __init__(self, *args, **kwargs):
            pass
        def get_performance_stats(self):
            return {}
        def clear_cache(self):
            pass
    
    AUDIO_ANALYSIS_AVAILABLE = False
    SOURCE_SEPARATION_AVAILABLE = False
    INSTRUMENT_CLASSIFICATION_AVAILABLE = False
    VISUALIZATION_AVAILABLE = False
    OPTIMIZATION_AVAILABLE = False

# Initialize FastMCP for Claude Desktop
mcp = FastMCP("IaraMCP - Análise Musical das Águas")

# Global instances
analyzer = AudioAnalyzer()
separator = SourceSeparator()
classifier = InstrumentClassifier()
visualizer = AudioVisualizer()
optimizer = PerformanceOptimizer(enable_cache=True) if OPTIMIZATION_AVAILABLE else PerformanceOptimizer()

# =============================================================================
# FERRAMENTAS MCP
# =============================================================================

@mcp.tool()
def iara_despertar(mensagem: str = "Olá") -> str:
    """Despertar da Iara - Testa a conexão e verifica o status de todos os módulos do servidor IaraMCP."""
    analysis_status = "✅ Fluindo" if AUDIO_ANALYSIS_AVAILABLE else "⚠️ Limitado"
    separation_status = "✅ Fluindo" if SOURCE_SEPARATION_AVAILABLE else "⚠️ Limitado"
    classification_status = "✅ Fluindo" if INSTRUMENT_CLASSIFICATION_AVAILABLE else "⚠️ Limitado"
    visualization_status = "✅ Fluindo" if VISUALIZATION_AVAILABLE else "⚠️ Limitado"
    optimization_status = "✅ Fluindo" if OPTIMIZATION_AVAILABLE else "⚠️ Limitado"
    return f"🧜‍♀️ IaraMCP está despertando das águas musicais! Análise: {analysis_status}, Separação: {separation_status}, Classificação: {classification_status}, Visualização: {visualization_status}, Otimização: {optimization_status}. Mensagem: {mensagem}"

@mcp.tool()
async def iara_mergulhar_nas_ondas(caminho_arquivo: str, tipo_analise: str = "completa") -> dict:
    """
    Mergulhar nas Ondas Musicais - Executa análise completa de características musicais (tempo, harmonia, espectro, ritmo) de arquivos de áudio usando algoritmos avançados.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        tipo_analise: Tipo de análise ('basica' ou 'completa')
    
    Returns:
        Análise abrangente incluindo características temporais, espectrais, harmônicas e rítmicas
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        # Validate audio file first
        validation = validate_audio_file(caminho_arquivo)
        if not validation.get("valid", False):
            return {"erro": f"Arquivo de áudio inválido: {validation}"}
        
        # Get basic info
        file_info = get_audio_info(caminho_arquivo)
        
        if tipo_analise == "basica":
            result = await analyzer.analyze_basic(caminho_arquivo)
        else:
            result = await analyzer.analyze_complete(caminho_arquivo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "tipo_analise": tipo_analise,
            "file_info": file_info,
            "analysis": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise musical: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
def iara_validar_cristais_sonoros(caminho_arquivo: str) -> dict:
    """
    Validar Cristais Sonoros - Verifica se um arquivo de áudio é válido e extrai metadados básicos (formato, duração, taxa de amostragem).
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
    
    Returns:
        Informações de validação e metadados do arquivo
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        validation = validate_audio_file(caminho_arquivo)
        file_info = get_audio_info(caminho_arquivo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "validacao": validation,
            "info_arquivo": file_info,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na validação: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

# Adicione mais ferramentas conforme necessário...

if __name__ == "__main__":
    mcp.run()