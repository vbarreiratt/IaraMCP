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

# PYTHONPATH is configured externally in Claude Desktop config

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

@mcp.tool()
async def iara_separar_instrumentos(caminho_arquivo: str, modelo: str = "htdemucs_ft") -> dict:
    """
    Separar Instrumentos - Separa e isola diferentes instrumentos/vozes de uma gravação musical usando IA.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        modelo: Modelo de separação ('htdemucs_ft', 'htdemucs', 'mdx_extra')
    
    Returns:
        Arquivos separados por instrumento com análise de qualidade
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await separator.separate_audio(caminho_arquivo, model_name=modelo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "modelo_usado": modelo,
            "separacao": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na separação de instrumentos: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_identificar_instrumentos(caminho_arquivo: str, confianca_minima: float = 0.7) -> dict:
    """
    Identificar Instrumentos - Identifica e classifica instrumentos presentes na gravação usando ML.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        confianca_minima: Confiança mínima para classificação (0.0-1.0)
    
    Returns:
        Lista de instrumentos identificados com níveis de confiança
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await classifier.identify_instruments(caminho_arquivo, min_confidence=confianca_minima)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "confianca_minima": confianca_minima,
            "instrumentos": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na identificação de instrumentos: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_visualizar_ondas(caminho_arquivo: str, tipo_visualizacao: str = "waveform") -> dict:
    """
    Visualizar Ondas - Cria visualizações gráficas do áudio (waveform, espectrograma, etc).
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        tipo_visualizacao: Tipo ('waveform', 'spectrogram', 'chromagram', 'mfcc')
    
    Returns:
        Caminho para arquivo de visualização gerada
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        output_path = definir_caminho_saida(f"iara_viz_{int(time.time())}", ".png")
        
        if tipo_visualizacao == "waveform":
            result = await visualizer.create_waveform(caminho_arquivo, output_path=output_path)
        elif tipo_visualizacao == "spectrogram":
            result = await visualizer.create_spectrogram(caminho_arquivo, output_path=output_path)
        elif tipo_visualizacao == "chromagram":
            result = await visualizer.create_chromagram(caminho_arquivo, output_path=output_path)
        elif tipo_visualizacao == "mfcc":
            result = await visualizer.create_mfcc(caminho_arquivo, output_path=output_path)
        else:
            return {"erro": f"Tipo de visualização inválido: {tipo_visualizacao}"}
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "tipo_visualizacao": tipo_visualizacao,
            "arquivo_saida": output_path,
            "resultado": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na visualização: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_extrair_melodia(caminho_arquivo: str, algoritmo: str = "melodia") -> dict:
    """
    Extrair Melodia - Extrai a melodia principal do áudio usando algoritmos avançados.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        algoritmo: Algoritmo de extração ('melodia', 'crepe', 'pyin')
    
    Returns:
        Sequência melódica extraída com informações de pitch
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.extract_melody(caminho_arquivo, algorithm=algoritmo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "algoritmo": algoritmo,
            "melodia": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na extração de melodia: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_detectar_acordes(caminho_arquivo: str, modo: str = "deep_chroma") -> dict:
    """
    Detectar Acordes - Detecta progressões de acordes na música usando análise harmônica.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        modo: Modo de detecção ('deep_chroma', 'nnls_chroma', 'crf')
    
    Returns:
        Sequência de acordes detectados com timestamps
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.detect_chords(caminho_arquivo, mode=modo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "modo": modo,
            "acordes": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na detecção de acordes: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_analisar_ritmo(caminho_arquivo: str, incluir_downbeats: bool = True) -> dict:
    """
    Analisar Ritmo - Analisa estrutura rítmica, tempo, beat tracking e patterns.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        incluir_downbeats: Se deve incluir detecção de downbeats
    
    Returns:
        Análise rítmica completa com BPM, beats e patterns
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.analyze_rhythm(caminho_arquivo, include_downbeats=incluir_downbeats)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "incluir_downbeats": incluir_downbeats,
            "analise_ritmica": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise rítmica: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_detectar_estrutura(caminho_arquivo: str, algoritmo: str = "laplacian") -> dict:
    """
    Detectar Estrutura - Detecta estrutura musical (verso, refrão, ponte, etc).
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        algoritmo: Algoritmo de segmentação ('laplacian', 'foote', 'olda')
    
    Returns:
        Segmentos estruturais da música com labels
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.detect_structure(caminho_arquivo, algorithm=algoritmo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "algoritmo": algoritmo,
            "estrutura": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na detecção de estrutura: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_analisar_timbre(caminho_arquivo: str, features: List[str] = None) -> dict:
    """
    Analisar Timbre - Analisa características timbrísticas (MFCC, spectral features, etc).
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        features: Features a extrair ['mfcc', 'spectral_centroid', 'spectral_rolloff', 'zcr']
    
    Returns:
        Análise detalhada de características timbrísticas
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        if features is None:
            features = ['mfcc', 'spectral_centroid', 'spectral_rolloff', 'zero_crossing_rate']
        
        result = await analyzer.analyze_timbre(caminho_arquivo, features=features)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "features": features,
            "analise_timbre": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise de timbre: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_detectar_key(caminho_arquivo: str, algoritmo: str = "krumhansl") -> dict:
    """
    Detectar Tonalidade - Detecta a tonalidade principal da música.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        algoritmo: Algoritmo de detecção ('krumhansl', 'temperley', 'edma')
    
    Returns:
        Tonalidade detectada com nível de confiança
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.detect_key(caminho_arquivo, algorithm=algoritmo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "algoritmo": algoritmo,
            "tonalidade": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na detecção de tonalidade: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_analisar_emocao(caminho_arquivo: str, modelo: str = "valence_arousal") -> dict:
    """
    Analisar Emoção - Analisa características emocionais da música (valência, energia, etc).
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        modelo: Modelo de análise ('valence_arousal', 'discrete_emotions', 'mood_classification')
    
    Returns:
        Análise emocional com métricas de valência e arousal
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.analyze_emotion(caminho_arquivo, model=modelo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "modelo": modelo,
            "analise_emocional": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise emocional: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_comparar_audios(arquivo1: str, arquivo2: str, metricas: List[str] = None) -> dict:
    """
    Comparar Áudios - Compara similaridade entre dois arquivos de áudio.
    
    Args:
        arquivo1: Caminho para o primeiro arquivo
        arquivo2: Caminho para o segundo arquivo
        metricas: Métricas de comparação ['mfcc_similarity', 'chroma_similarity', 'spectral_similarity']
    
    Returns:
        Análise de similaridade com scores para diferentes aspectos
    """
    try:
        if not Path(arquivo1).exists():
            return {"erro": f"Primeiro arquivo não encontrado: {arquivo1}"}
        if not Path(arquivo2).exists():
            return {"erro": f"Segundo arquivo não encontrado: {arquivo2}"}
        
        if metricas is None:
            metricas = ['mfcc_similarity', 'chroma_similarity', 'spectral_similarity']
        
        result = await analyzer.compare_audio(arquivo1, arquivo2, metrics=metricas)
        
        return {
            "arquivo1": arquivo1,
            "arquivo2": arquivo2,
            "metricas": metricas,
            "similaridade": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na comparação de áudios: {str(e)}",
            "arquivos": [arquivo1, arquivo2]
        }

@mcp.tool()
async def iara_extrair_features_ml(caminho_arquivo: str, feature_set: str = "comprehensive") -> dict:
    """
    Extrair Features ML - Extrai features otimizadas para machine learning.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        feature_set: Conjunto de features ('basic', 'comprehensive', 'minimal')
    
    Returns:
        Conjunto de features vetorizadas para ML
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.extract_ml_features(caminho_arquivo, feature_set=feature_set)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "feature_set": feature_set,
            "features": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na extração de features ML: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_classificar_genero(caminho_arquivo: str, modelo: str = "deep_learning") -> dict:
    """
    Classificar Gênero - Classifica o gênero musical usando machine learning.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        modelo: Modelo de classificação ('deep_learning', 'traditional_ml', 'ensemble')
    
    Returns:
        Classificação de gênero com probabilidades
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await classifier.classify_genre(caminho_arquivo, model=modelo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "modelo": modelo,
            "classificacao_genero": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na classificação de gênero: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_detectar_onset(caminho_arquivo: str, algoritmo: str = "default") -> dict:
    """
    Detectar Onset - Detecta início de notas/eventos musicais.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        algoritmo: Algoritmo de detecção ('default', 'energy', 'hfc', 'complex')
    
    Returns:
        Timestamps de onsets detectados
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.detect_onset(caminho_arquivo, algorithm=algoritmo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "algoritmo": algoritmo,
            "onsets": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na detecção de onset: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_analisar_loudness(caminho_arquivo: str, standard: str = "lufs") -> dict:
    """
    Analisar Loudness - Analisa loudness usando padrões da indústria.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        standard: Padrão de medição ('lufs', 'rms', 'peak')
    
    Returns:
        Análise de loudness com métricas da indústria
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.analyze_loudness(caminho_arquivo, standard=standard)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "standard": standard,
            "analise_loudness": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise de loudness: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_segmentar_audio(caminho_arquivo: str, tipo_segmentacao: str = "auto") -> dict:
    """
    Segmentar Áudio - Segmenta áudio em seções baseadas em mudanças musicais.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        tipo_segmentacao: Tipo ('auto', 'fixed_duration', 'beat_sync', 'structure_based')
    
    Returns:
        Segmentos de áudio com timestamps e características
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.segment_audio(caminho_arquivo, segmentation_type=tipo_segmentacao)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "tipo_segmentacao": tipo_segmentacao,
            "segmentos": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na segmentação de áudio: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
async def iara_analisar_dinamica(caminho_arquivo: str, janela_tempo: float = 1.0) -> dict:
    """
    Analisar Dinâmica - Analisa variações dinâmicas e dinâmica temporal.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        janela_tempo: Janela de tempo para análise em segundos
    
    Returns:
        Análise de dinâmica com variações temporais
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        result = await analyzer.analyze_dynamics(caminho_arquivo, time_window=janela_tempo)
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "janela_tempo": janela_tempo,
            "analise_dinamica": result,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na análise de dinâmica: {str(e)}",
            "caminho_arquivo": caminho_arquivo
        }

@mcp.tool()
def iara_otimizar_performance() -> dict:
    """
    Otimizar Performance - Limpa cache e otimiza performance do sistema.
    
    Returns:
        Status das operações de otimização
    """
    try:
        optimizer.clear_cache()
        stats = optimizer.get_performance_stats()
        
        return {
            "operacao": "otimizacao_performance",
            "cache_limpo": True,
            "estatisticas": stats,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return {
            "erro": f"Falha na otimização: {str(e)}"
        }

@mcp.tool()
def iara_listar_ferramentas() -> dict:
    """
    Listar Ferramentas - Lista todas as ferramentas disponíveis da Iara com suas descrições temáticas.
    
    Returns:
        Dicionário com todas as ferramentas e suas capacidades
    """
    ferramentas = {
        "despertar": {"nome": "iara_despertar", "descricao": "Status do servidor e módulos"},
        "mergulhar_ondas": {"nome": "iara_mergulhar_nas_ondas", "descricao": "Análise musical completa"},
        "validar_cristais": {"nome": "iara_validar_cristais_sonoros", "descricao": "Validação de arquivos"},
        "separar_instrumentos": {"nome": "iara_separar_instrumentos", "descricao": "Separação de fontes"},
        "identificar_instrumentos": {"nome": "iara_identificar_instrumentos", "descricao": "Classificação de instrumentos"},
        "visualizar_ondas": {"nome": "iara_visualizar_ondas", "descricao": "Visualizações gráficas"},
        "extrair_melodia": {"nome": "iara_extrair_melodia", "descricao": "Extração melódica"},
        "detectar_acordes": {"nome": "iara_detectar_acordes", "descricao": "Análise harmônica"},
        "analisar_ritmo": {"nome": "iara_analisar_ritmo", "descricao": "Análise rítmica"},
        "detectar_estrutura": {"nome": "iara_detectar_estrutura", "descricao": "Segmentação estrutural"},
        "analisar_timbre": {"nome": "iara_analisar_timbre", "descricao": "Análise timbrística"},
        "detectar_key": {"nome": "iara_detectar_key", "descricao": "Detecção de tonalidade"},
        "analisar_emocao": {"nome": "iara_analisar_emocao", "descricao": "Análise emocional"},
        "comparar_audios": {"nome": "iara_comparar_audios", "descricao": "Análise de similaridade"},
        "extrair_features_ml": {"nome": "iara_extrair_features_ml", "descricao": "Features para ML"},
        "classificar_genero": {"nome": "iara_classificar_genero", "descricao": "Classificação de gênero"},
        "detectar_onset": {"nome": "iara_detectar_onset", "descricao": "Detecção de onset"},
        "analisar_loudness": {"nome": "iara_analisar_loudness", "descricao": "Análise de loudness"},
        "segmentar_audio": {"nome": "iara_segmentar_audio", "descricao": "Segmentação de áudio"},
        "analisar_dinamica": {"nome": "iara_analisar_dinamica", "descricao": "Análise dinâmica"},
        "otimizar_performance": {"nome": "iara_otimizar_performance", "descricao": "Otimização do sistema"}
    }
    
    return {
        "ferramentas_iara": ferramentas,
        "total_ferramentas": len(ferramentas),
        "status_modulos": {
            "audio_analysis": AUDIO_ANALYSIS_AVAILABLE,
            "source_separation": SOURCE_SEPARATION_AVAILABLE,
            "instrument_classification": INSTRUMENT_CLASSIFICATION_AVAILABLE,
            "visualization": VISUALIZATION_AVAILABLE,
            "optimization": OPTIMIZATION_AVAILABLE
        },
        "mensagem": "🧜‍♀️ A Iara tem todas essas ferramentas mágicas para analisar as águas musicais!"
    }

if __name__ == "__main__":
    mcp.run()