#!/usr/bin/env python3
"""
IaraMCP - Servidor de Análise Musical Avançada
Inspirado na Iara, ser mitológico brasileiro das águas.
Implementa análise musical completa via protocolo MCP.
"""

from fastapi import FastAPI
from fastmcp import FastMCP
from pathlib import Path
import json
import sys
import os
import asyncio
import time
import logging
from typing import Dict, List, Optional, Any



# Função para detectar o modo de visualização (mover aqui para evitar importação circular)
def detectar_modo_visualizacao() -> str:
    """
    Detecta o modo de visualização do ambiente.
    Retorna "local" se estiver em ambiente desktop, "web" caso contrário.
    """
    # Heurística simples baseada em variáveis de ambiente ou contexto
    # Pode ser expandida conforme necessário
    if os.environ.get("IARAMCP_VIS_MODE") == "local":
        return "local"
    # Detecta se está rodando em ambiente Jupyter ou Google Colab
    try:
        import IPython
        if "google.colab" in str(getattr(IPython, "get_ipython", lambda: None)()):
            return "web"
    except Exception:
        pass
    # Fallback: se tiver DISPLAY ou rodando em desktop
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
    # Fallback - create dummy functions for testing
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
        async def analyze_stem_quality(self, stem_path):
            return {"error": "Source separation not available - missing dependencies"}
        @classmethod
        def get_available_models(cls):
            return {}
    
    class InstrumentClassifier:
        async def identify_instruments(self, file_path, **kwargs):
            return {"error": "Instrument classification not available - missing dependencies"}
        @classmethod
        def get_supported_instruments(cls):
            return {}
        @classmethod
        def get_feature_importance(cls):
            return {}
    
    class AudioVisualizer:
        async def create_waveform(self, file_path, **kwargs):
            return {"error": "Visualization not available - missing dependencies"}
        async def create_spectrogram(self, file_path, **kwargs):
            return {"error": "Visualization not available - missing dependencies"}
        async def create_feature_analysis_plot(self, features, **kwargs):
            return {"error": "Visualization not available - missing dependencies"}
        async def create_stems_comparison(self, stems_data, **kwargs):
            return {"error": "Visualization not available - missing dependencies"}
        @classmethod
        def get_supported_plot_types(cls):
            return []
        @classmethod
        def get_plot_descriptions(cls):
            return {}
    
    class PerformanceOptimizer:
        def __init__(self, *args, **kwargs):
            pass
        async def run_with_cache(self, *args, **kwargs):
            return {"error": "Optimization not available - missing dependencies"}
        def get_performance_stats(self):
            return {}
        def clear_cache(self):
            pass
    
    AUDIO_ANALYSIS_AVAILABLE = False
    SOURCE_SEPARATION_AVAILABLE = False
    INSTRUMENT_CLASSIFICATION_AVAILABLE = False
    VISUALIZATION_AVAILABLE = False
    OPTIMIZATION_AVAILABLE = False

# =========================================================
# ===> ESTRUTURA DA APLICAÇÃO ATUALIZADA <===
# =========================================================

# =========================================================
# ===> CORREÇÃO PARA CLAUDE DESKTOP <===
# =========================================================

# Para Claude Desktop, usamos apenas FastMCP diretamente
mcp = FastMCP("IaraMCP - Análise Musical das Águas")

# Para Claude Desktop, app = mcp (sem FastAPI)
app = mcp

# Global instances
analyzer = AudioAnalyzer() if AUDIO_ANALYSIS_AVAILABLE else AudioAnalyzer()
separator = SourceSeparator() if SOURCE_SEPARATION_AVAILABLE else SourceSeparator()
classifier = InstrumentClassifier() if INSTRUMENT_CLASSIFICATION_AVAILABLE else InstrumentClassifier()
visualizer = AudioVisualizer() if VISUALIZATION_AVAILABLE else AudioVisualizer()
optimizer = PerformanceOptimizer(enable_cache=True) if OPTIMIZATION_AVAILABLE else PerformanceOptimizer()

# =============================================================================
# CORE MCP TOOLS AS PER PROJECT SPECIFICATIONS
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
        
        # Perform analysis based on type
        if tipo_analise.lower() == "basica":
            result = await analyzer.analyze_basic(caminho_arquivo)
        else:
            result = await analyzer.analyze_complete(caminho_arquivo)
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "erro": f"Análise falhou: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_validar_cristais_sonoros(caminho_arquivo: str) -> dict:
    """
    Validar Cristais Sonoros - Verifica se um arquivo de áudio é válido (MP3, WAV, FLAC, M4A, OGG) e extrai metadados básicos como duração, formato e tamanho.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
    
    Returns:
        Resultados da validação e informações básicas do arquivo
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        validation = validate_audio_file(caminho_arquivo)
        file_info = get_audio_info(caminho_arquivo) if AUDIO_ANALYSIS_AVAILABLE else {}
        
        return {
            "caminho_arquivo": caminho_arquivo,
            "validacao": validation,
            "info_arquivo": file_info,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
    except Exception as e:
        return {"error": f"Validation failed: {str(e)}"}

@mcp.tool()
async def iara_tecer_relatorio_das_aguas(file_path: str, format: str = "json", include_visualizations: bool = False) -> dict:
    """
    Tecer Relatório das Águas - Gera relatório completo e formatado (JSON/texto) com análise musical detalhada, incluindo opcionalmente visualizações gráficas.
    
    Args:
        file_path: Path to the audio file
        format: Output format ('json' or 'text')
        include_visualizations: Whether to include visualization data
    
    Returns:
        Complete music analysis report
    """
    try:
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        # Get complete analysis
        analysis = await analyzer.analyze_complete(file_path)
        
        if "error" in analysis:
            return analysis
        
        # Generate report
        report = {
            "report_metadata": {
                "generated_at": time.strftime('%Y-%m-%d %H:%M:%S'),
                "file_path": file_path,
                "format": format,
                "analysis_version": "1.0"
            },
            "file_info": analysis.get("metadata", {}),
            "musical_analysis": analysis.get("analysis", {}),
            "summary": await _generate_summary(analysis),
            "recommendations": await _generate_recommendations(analysis)
        }
        
        if include_visualizations:
            report["visualizations"] = {
                "note": "Visualization data would be included here",
                "available_plots": ["waveform", "spectrogram", "chroma", "tempo_curve"]
            }
        
        return report
        
    except Exception as e:
        import traceback
        return {
            "error": f"Report generation failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_explorar_caverna_sonora(directory_path: str, file_extensions: List[str] = [".mp3", ".wav", ".m4a"]) -> dict:
    """
    Explorar Caverna Sonora - Processa em lote múltiplos arquivos de áudio em um diretório, executando análise musical em cada arquivo encontrado.
    
    Args:
        directory_path: Path to directory containing audio files
        file_extensions: List of file extensions to process
    
    Returns:
        Batch analysis results
    """
    try:
        dir_path = Path(directory_path)
        if not dir_path.exists():
            return {"error": f"Directory not found: {directory_path}"}
        
        # Find audio files
        audio_files = []
        for ext in file_extensions:
            audio_files.extend(dir_path.glob(f"*{ext}"))
            audio_files.extend(dir_path.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            return {
                "error": f"No audio files found with extensions {file_extensions}",
                "directory": directory_path
            }
        
        # For now, return file list - full batch processing would be implemented later
        return {
            "directory_path": directory_path,
            "found_files": [str(f) for f in audio_files[:10]],  # Limit to first 10
            "total_files": len(audio_files),
            "supported_extensions": file_extensions,
            "note": "Full batch processing will be implemented in Phase 2",
            "next_step": "Use analyze_musical_features on individual files"
        }
        
    except Exception as e:
        return {"error": f"Directory analysis failed: {str(e)}"}

# =============================================================================
# SOURCE SEPARATION TOOLS (PHASE 2)
# =============================================================================

@mcp.tool()
async def iara_separar_correntes_musicais(
    caminho_arquivo: str,
    metodo: str = "demucs",
    modelo: str = "htdemucs_ft",
    formato_saida: str = "wav",
    diretorio_saida: Optional[str] = None
) -> dict:
    """
    Separar Correntes Musicais - Executa separação de fontes usando modelos Demucs, dividindo áudio em stems isolados (vocals, drums, bass, other) com qualidade profissional.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        metodo: Método de separação ('demucs' apenas por enquanto)
        modelo: Modelo Demucs a usar (htdemucs_ft, htdemucs, hdemucs_mmi, mdx)
        formato_saida: Formato de saída (wav, mp3, flac)
        diretorio_saida: Diretório para salvar streams (None para diretório temporário)
    
    Returns:
        Separation results with stem paths and quality metrics
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"error": f"File not found: {caminho_arquivo}"}

        if metodo.lower() != "demucs":
            return {"error": f"Unsupported separation method: {metodo}. Only 'demucs' is supported."}

        # Validate model
        available_models = SourceSeparator.get_available_models()
        if modelo not in available_models:
            return {
                "error": f"Unsupported model: {modelo}",
                "available_models": available_models
            }

        # Fallback automático para modo de execução (Claude Desktop etc)
        if diretorio_saida is None:
            try:
                from iaramcp.utils.environment import detectar_modo_execucao
                modo = detectar_modo_execucao()
            except Exception:
                modo = "modo_local"
            if modo == "modo_local":
                diretorio_saida = os.path.join("/Users/vitor/Desktop", "stems_separados")
            else:
                diretorio_saida = None

        # Create separator with specified model
        local_separator = SourceSeparator(model_name=modelo, device='auto')

        # Progress callback for user feedback
        async def progress_update(message: str, percent: int):
            pass  # Could be enhanced to provide real-time updates

        # Perform separation
        result = await local_separator.separate_audio(
            file_path=caminho_arquivo,
            output_dir=diretorio_saida,
            format=formato_saida,
            progress_callback=progress_update
        )

        return result

    except Exception as e:
        import traceback
        return {
            "error": f"Audio separation failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_examinar_corrente_isolada(stem_path: str, instrument_type: str = "auto") -> dict:
    """
    Examinar Corrente Isolada - Analisa em detalhes um stem individual (vocal, bateria, baixo, outros) já separado, extraindo características específicas do instrumento.
    
    Args:
        stem_path: Path to the stem audio file
        instrument_type: Type of instrument (auto, vocals, drums, bass, other)
    
    Returns:
        Detailed analysis of the stem
    """
    try:
        if not Path(stem_path).exists():
            return {"error": f"Stem file not found: {stem_path}"}
        
        # Analyze stem quality
        quality_result = await separator.analyze_stem_quality(stem_path)
        
        if "error" in quality_result:
            return quality_result
        
        # Perform musical analysis on the stem
        analysis_result = await analyzer.analyze_complete(stem_path)
        
        if "error" in analysis_result:
            return analysis_result
        
        # Combine results
        combined_result = {
            "stem_info": {
                "file_path": stem_path,
                "instrument_type": instrument_type,
                "analysis_timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            },
            "quality_analysis": quality_result.get("quality_metrics", {}),
            "musical_analysis": analysis_result.get("analysis", {}),
            "stem_characteristics": await _analyze_stem_characteristics(
                analysis_result.get("analysis", {}), 
                instrument_type
            )
        }
        
        return combined_result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Stem analysis failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_comparar_magias_separadoras(
    file_path: str, 
    methods: List[str] = ["htdemucs_ft", "htdemucs"],
    metrics: List[str] = ["quality", "speed"]
) -> dict:
    """
    Comparar Magias Separadoras - Testa e compara múltiplos modelos de separação de fontes (htdemucs_ft, htdemucs) no mesmo arquivo, avaliando qualidade e velocidade.
    
    Args:
        file_path: Path to the audio file
        methods: List of Demucs models to compare
        metrics: Metrics to compare (quality, speed, etc.)
    
    Returns:
        Comparison results between different methods
    """
    try:
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        available_models = SourceSeparator.get_available_models()
        valid_methods = [m for m in methods if m in available_models]
        
        if not valid_methods:
            return {
                "error": "No valid models specified",
                "available_models": available_models,
                "requested_methods": methods
            }
        
        comparison_results = {
            "input_file": file_path,
            "compared_models": valid_methods,
            "metrics": metrics,
            "results": {},
            "summary": {}
        }
        
        # Test each method
        for model in valid_methods:
            start_time = time.time()
            
            # Create separator for this model
            model_separator = SourceSeparator(model_name=model, device='auto')
            
            # Perform separation
            result = await model_separator.separate_audio(
                file_path=file_path,
                output_dir=None,  # Use temp directory
                format='wav'
            )
            
            processing_time = time.time() - start_time
            
            if "error" not in result:
                # Calculate quality scores
                quality_score = await _calculate_separation_quality(result)
                
                comparison_results["results"][model] = {
                    "processing_time_seconds": processing_time,
                    "quality_score": quality_score,
                    "stems_quality": result.get("separation", {}).get("quality_metrics", {}),
                    "success": True
                }
                
                # Cleanup temp files
                metadata = result.get("metadata", {})
                if metadata.get("temporary_directory", False):
                    output_dir = metadata.get("output_directory")
                    if output_dir:
                        model_separator.cleanup_temp_files(output_dir)
            else:
                comparison_results["results"][model] = {
                    "processing_time_seconds": processing_time,
                    "error": result["error"],
                    "success": False
                }
        
        # Generate summary
        successful_results = {k: v for k, v in comparison_results["results"].items() if v.get("success", False)}
        
        if successful_results:
            # Find best model by quality
            best_quality = max(successful_results.items(), key=lambda x: x[1].get("quality_score", 0))
            fastest = min(successful_results.items(), key=lambda x: x[1].get("processing_time_seconds", float('inf')))
            
            comparison_results["summary"] = {
                "best_quality": {"model": best_quality[0], "score": best_quality[1].get("quality_score", 0)},
                "fastest": {"model": fastest[0], "time": fastest[1].get("processing_time_seconds", 0)},
                "recommendation": best_quality[0] if best_quality[1].get("quality_score", 0) > 0.7 else fastest[0]
            }
        
        return comparison_results
        
    except Exception as e:
        import traceback
        return {
            "error": f"Method comparison failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_revelar_segredos_separacao() -> dict:
    """
    Revelar Segredos da Separação - Lista todos os modelos de separação de fontes disponíveis, suas capacidades e configurações de sistema.
    
    Returns:
        Available models, formats, and system information
    """
    try:
        import torch
        
        device_info = {
            "cuda_available": torch.cuda.is_available(),
            "mps_available": hasattr(torch.backends, 'mps') and torch.backends.mps.is_available(),
            "recommended_device": separator.device if hasattr(separator, 'device') else 'cpu'
        }
        
        if torch.cuda.is_available():
            device_info["cuda_device_count"] = torch.cuda.device_count()
            device_info["cuda_device_name"] = torch.cuda.get_device_name(0)
        
        return {
            "separation_available": SOURCE_SEPARATION_AVAILABLE,
            "available_models": SourceSeparator.get_available_models(),
            "supported_formats": SourceSeparator.get_supported_formats(),
            "device_info": device_info,
            "stems": SourceSeparator.STEMS,
            "recommendations": {
                "best_quality": "htdemucs_ft",
                "fastest": "mdx",
                "balanced": "htdemucs",
                "vocals_focused": "mdx_extra"
            }
        }
        
    except Exception as e:
        return {
            "separation_available": SOURCE_SEPARATION_AVAILABLE,
            "error": f"Failed to get system info: {str(e)}"
        }

# =============================================================================
# INSTRUMENT CLASSIFICATION TOOLS (PHASE 3)
# =============================================================================

@mcp.tool()
async def iara_reconhecer_instrumentos_das_aguas(
    caminho_arquivo: str,
    usar_separacao: bool = True,
    limiar_confianca: float = 0.7,
    metodo: str = "heuristico"
) -> dict:
    """
    Reconhecer Instrumentos das Águas - Detecta e classifica instrumentos musicais presentes no áudio usando análise espectral e machine learning, com scores de confiança configuráveis.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        usar_separacao: Usar streams separados para melhor precisão
        limiar_confianca: Confiança mínima para detecção de instrumentos (0.0-1.0)
        metodo: Método de detecção ('heuristico', 'ml', 'hibrido')
    
    Returns:
        Detected instruments with confidence scores and subcategories
    """
    try:
        if not Path(caminho_arquivo).exists():
            return {"error": f"File not found: {caminho_arquivo}"}
        
        result = await classifier.identify_instruments(
            file_path=caminho_arquivo,
            use_separation=usar_separacao,
            confidence_threshold=limiar_confianca,
            method=metodo
        )
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Instrument identification failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_identificar_voz_das_aguas(stem_path: str, expected_type: str = "auto") -> dict:
    """
    Identificar Voz das Águas - Classifica automaticamente o tipo de instrumento presente em um stem separado (vocal, bateria, baixo, etc).
    
    Args:
        stem_path: Path to the stem audio file
        expected_type: Expected instrument type for validation (auto, vocals, drums, bass, other)
    
    Returns:
        Classification results with confidence and subtype
    """
    try:
        if not Path(stem_path).exists():
            return {"error": f"Stem file not found: {stem_path}"}
        
        # Use the classifier on individual stem
        result = await classifier.identify_instruments(
            file_path=stem_path,
            use_separation=False,  # Already a stem
            confidence_threshold=0.5,  # Lower threshold for stems
            method="heuristic"
        )
        
        if "error" in result:
            return result
        
        # Add stem-specific analysis
        stem_result = {
            "stem_path": stem_path,
            "expected_type": expected_type,
            "classification": result,
            "validation": {}
        }
        
        # Validate against expected type if provided
        if expected_type != "auto":
            detected_types = [inst["type"] for inst in result.get("detected_instruments", [])]
            stem_result["validation"] = {
                "matches_expected": expected_type in detected_types,
                "confidence_match": any(
                    inst["type"] == expected_type and inst["confidence"] > 0.7 
                    for inst in result.get("detected_instruments", [])
                )
            }
        
        return stem_result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Stem classification failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_revelar_alma_do_instrumento(file_path: str, instrument_type: str) -> dict:
    """
    Revelar Alma do Instrumento - Extrai perfil detalhado de um instrumento específico detectado no áudio, incluindo características tímbricas e espectrais.
    
    Args:
        file_path: Path to the audio file
        instrument_type: Type of instrument to profile (vocals, drums, bass, etc.)
    
    Returns:
        Detailed instrument profile with characteristics and recommendations
    """
    try:
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        # First identify all instruments
        identification = await classifier.identify_instruments(
            file_path=file_path,
            use_separation=False,
            confidence_threshold=0.3,  # Lower threshold for profiling
            method="heuristic"
        )
        
        if "error" in identification:
            return identification
        
        # Find the specific instrument
        target_instrument = None
        for instrument in identification.get("detected_instruments", []):
            if instrument["type"] == instrument_type:
                target_instrument = instrument
                break
        
        if not target_instrument:
            return {
                "error": f"Instrument '{instrument_type}' not detected in audio",
                "detected_instruments": [inst["type"] for inst in identification.get("detected_instruments", [])]
            }
        
        # Create detailed profile
        profile = {
            "instrument_type": instrument_type,
            "subtype": target_instrument.get("subtype", "unknown"),
            "confidence": target_instrument.get("confidence", 0.0),
            "characteristics": await _generate_instrument_characteristics(
                identification.get("instrument_analysis", {}), 
                instrument_type
            ),
            "production_tips": await _generate_production_tips(instrument_type, target_instrument),
            "frequency_profile": await _generate_frequency_profile(
                identification.get("instrument_analysis", {}), 
                instrument_type
            )
        }
        
        return profile
        
    except Exception as e:
        import traceback
        return {
            "error": f"Instrument profiling failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_mostrar_sabedoria_classificadora() -> dict:
    """
    Mostrar Sabedoria Classificadora - Lista todos os instrumentos que podem ser classificados pelo sistema e métodos de classificação disponíveis.
    
    Returns:
        Available instruments, methods, and system information
    """
    try:
        return {
            "classification_available": INSTRUMENT_CLASSIFICATION_AVAILABLE,
            "supported_instruments": InstrumentClassifier.get_supported_instruments(),
            "detection_methods": ["heuristic", "ml", "hybrid"],
            "feature_importance": InstrumentClassifier.get_feature_importance(),
            "confidence_thresholds": {
                "high_precision": 0.8,
                "balanced": 0.7,
                "high_recall": 0.5,
                "exploratory": 0.3
            },
            "recommendations": {
                "vocals": "Use stems for better accuracy, mid-frequency analysis",
                "drums": "Percussive energy detection, rhythm analysis",
                "bass": "Low-frequency dominance, harmonic content",
                "synth": "Spectral analysis, electronic characteristics"
            }
        }
        
    except Exception as e:
        return {
            "classification_available": INSTRUMENT_CLASSIFICATION_AVAILABLE,
            "error": f"Failed to get classification info: {str(e)}"
        }

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

async def _generate_summary(analysis: dict) -> dict:
    """Generate a human-readable summary of the analysis."""
    try:
        metadata = analysis.get("metadata", {})
        analysis_data = analysis.get("analysis", {})
        
        temporal = analysis_data.get("temporal", {})
        spectral = analysis_data.get("spectral", {})
        harmonic = analysis_data.get("harmonic", {})
        rhythmic = analysis_data.get("rhythmic", {})
        
        # Determine genre hints based on features
        tempo = temporal.get("tempo_bpm", 0)
        genre_hints = []
        
        if 60 <= tempo <= 80:
            genre_hints.append("ballad/slow")
        elif 80 <= tempo <= 100:
            genre_hints.append("pop/rock")
        elif 100 <= tempo <= 130:
            genre_hints.append("pop/dance")
        elif 130 <= tempo <= 150:
            genre_hints.append("hip-hop/trap")
        elif tempo > 150:
            genre_hints.append("electronic/house")
        
        # Energy level
        rms_energy = spectral.get("rms_energy", {}).get("mean", 0)
        energy_level = "high" if rms_energy > 0.1 else "medium" if rms_energy > 0.05 else "low"
        
        return {
            "duration": metadata.get("duration_formatted", "unknown"),
            "tempo_bpm": tempo,
            "estimated_key": harmonic.get("estimated_key", "unknown"),
            "energy_level": energy_level,
            "genre_hints": genre_hints,
            "complexity": {
                "rhythmic": rhythmic.get("rhythm_complexity", 0),
                "harmonic": harmonic.get("key_confidence", 0),
                "spectral_richness": spectral.get("spectral_bandwidth", {}).get("mean", 0)
            }
        }
    except Exception as e:
        return {"error": f"Summary generation failed: {str(e)}"}

async def _generate_recommendations(analysis: dict) -> dict:
    """Generate production and analysis recommendations."""
    try:
        analysis_data = analysis.get("analysis", {})
        temporal = analysis_data.get("temporal", {})
        spectral = analysis_data.get("spectral", {})
        harmonic = analysis_data.get("harmonic", {})
        
        recommendations = {
            "production_notes": [],
            "similar_analysis": [],
            "next_steps": []
        }
        
        # Production recommendations based on analysis
        if temporal.get("beat_consistency", 0) < 0.7:
            recommendations["production_notes"].append("Consider using a metronome - timing inconsistencies detected")
        
        if spectral.get("rms_energy", {}).get("dynamic_range", 0) < 0.1:
            recommendations["production_notes"].append("Low dynamic range - consider varying the energy levels")
        
        # Next steps recommendations
        recommendations["next_steps"].extend([
            "Consider using source separation for detailed instrument analysis",
            "Analyze individual stems for better instrument identification",
            "Compare with reference tracks in similar genre"
        ])
        
        return recommendations
    except Exception as e:
        return {"error": f"Recommendations generation failed: {str(e)}"}

async def _analyze_stem_characteristics(analysis: dict, instrument_type: str) -> dict:
    """Analyze stem-specific characteristics."""
    try:
        temporal = analysis.get("temporal", {})
        spectral = analysis.get("spectral", {})
        harmonic = analysis.get("harmonic", {})
        rhythmic = analysis.get("rhythmic", {})
        
        characteristics = {
            "instrument_type": instrument_type,
            "dominant_features": [],
            "quality_indicators": {}
        }
        
        # Instrument-specific analysis
        if instrument_type == "vocals":
            # Vocals typically have mid-frequency content and harmonic structure
            mid_energy = spectral.get("spectral_centroid", {}).get("mean", 0)
            harmonic_energy = harmonic.get("harmonic_energy", 0)
            
            characteristics["quality_indicators"] = {
                "mid_frequency_presence": mid_energy > 1000,
                "harmonic_content": harmonic_energy > 0.1,
                "vocal_range_estimate": "mid" if 500 <= mid_energy <= 3000 else "outside_typical"
            }
            
        elif instrument_type == "drums":
            # Drums have strong percussive energy and transients
            percussive_energy = harmonic.get("percussive_energy", 0)
            onset_rate = temporal.get("onset_rate_per_second", 0)
            
            characteristics["quality_indicators"] = {
                "percussive_strength": percussive_energy > 0.1,
                "transient_density": onset_rate,
                "rhythm_clarity": rhythmic.get("tempo_stability", 0)
            }
            
        elif instrument_type == "bass":
            # Bass has low-frequency energy
            low_energy = rhythmic.get("low_freq_energy", 0)
            
            characteristics["quality_indicators"] = {
                "low_frequency_dominance": low_energy > 0.1,
                "bass_prominence": rhythmic.get("rhythm_balance", {}).get("bass_prominence", 0)
            }
            
        else:  # other instruments
            characteristics["quality_indicators"] = {
                "harmonic_richness": harmonic.get("harmonic_energy", 0),
                "spectral_complexity": spectral.get("spectral_bandwidth", {}).get("mean", 0)
            }
        
        return characteristics
        
    except Exception as e:
        return {"error": f"Stem characteristics analysis failed: {str(e)}"}

async def _calculate_separation_quality(separation_result: dict) -> float:
    """Calculate overall quality score for separation result."""
    try:
        quality_metrics = separation_result.get("separation", {}).get("quality_metrics", {})
        
        if not quality_metrics:
            return 0.0
        
        # Calculate weighted quality score based on stem energies and confidence
        total_score = 0.0
        total_weight = 0.0
        
        for stem_name, metrics in quality_metrics.items():
            confidence = metrics.get("confidence", 0.0)
            rms_energy = metrics.get("rms_energy", 0.0)
            
            # Weight by confidence and energy
            weight = confidence * (1.0 + rms_energy)
            total_score += confidence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        overall_quality = total_score / total_weight
        return min(1.0, overall_quality)  # Cap at 1.0
        
    except Exception as e:
        logger.warning(f"Quality calculation failed: {e}")
        return 0.5  # Default quality score

async def _generate_instrument_characteristics(analysis: dict, instrument_type: str) -> dict:
    """Generate detailed characteristics for a specific instrument."""
    try:
        spectral = analysis.get("spectral", {})
        freq_bands = analysis.get("frequency_bands", {})
        hpss = analysis.get("hpss", {})
        energy = analysis.get("energy", {})
        
        characteristics = {
            "frequency_range": {},
            "timbral_qualities": {},
            "dynamic_properties": {},
            "harmonic_content": {}
        }
        
        if instrument_type == "vocals":
            characteristics.update({
                "frequency_range": {
                    "fundamental_range": "80-1100 Hz",
                    "formant_range": "300-3400 Hz",
                    "presence_detected": spectral.get("centroid_mean", 0) > 1000
                },
                "timbral_qualities": {
                    "brightness": spectral.get("centroid_mean", 0) / 4000,
                    "warmth": freq_bands.get("low_mid_energy", 0),
                    "clarity": freq_bands.get("mid_energy", 0)
                }
            })
        elif instrument_type == "drums":
            characteristics.update({
                "frequency_range": {
                    "kick_range": freq_bands.get("bass_energy", 0),
                    "snare_range": freq_bands.get("mid_energy", 0),
                    "cymbals_range": freq_bands.get("high_energy", 0)
                },
                "dynamic_properties": {
                    "transient_strength": hpss.get("percussive_energy", 0),
                    "sustain_ratio": hpss.get("harmonic_energy", 0) / (hpss.get("percussive_energy", 0) + 1e-8)
                }
            })
        elif instrument_type == "bass":
            characteristics.update({
                "frequency_range": {
                    "sub_bass": "20-60 Hz presence",
                    "bass_fundamentals": "60-250 Hz",
                    "low_mid_harmonics": "250-500 Hz"
                },
                "timbral_qualities": {
                    "punch": freq_bands.get("bass_energy", 0),
                    "definition": freq_bands.get("low_mid_energy", 0)
                }
            })
        
        return characteristics
        
    except Exception as e:
        return {"error": f"Characteristics generation failed: {str(e)}"}

async def _generate_production_tips(instrument_type: str, instrument_data: dict) -> dict:
    """Generate production tips for the detected instrument."""
    try:
        tips = {
            "eq_suggestions": [],
            "processing_tips": [],
            "mixing_advice": []
        }
        
        confidence = instrument_data.get("confidence", 0.0)
        subtype = instrument_data.get("subtype", "unknown")
        
        if instrument_type == "vocals":
            tips["eq_suggestions"] = [
                "High-pass filter around 80-100 Hz to remove low-end rumble",
                "Boost presence around 2-5 kHz for clarity",
                "De-ess around 6-8 kHz if sibilance is present"
            ]
            tips["processing_tips"] = [
                "Use compression with 3:1 ratio for consistent level",
                "Add subtle reverb for space and depth",
                "Consider pitch correction if needed"
            ]
        elif instrument_type == "drums":
            tips["eq_suggestions"] = [
                "Boost kick drum around 60-80 Hz for weight",
                "Add snap to snare around 2-4 kHz",
                "Control cymbals with high-shelf EQ"
            ]
            tips["processing_tips"] = [
                "Use parallel compression for punch",
                "Gate tom and cymbal tracks to reduce bleed",
                "Add reverb to snare for size"
            ]
        elif instrument_type == "bass":
            tips["eq_suggestions"] = [
                "High-pass below 30 Hz to remove sub-sonic content",
                "Shape fundamental around 60-100 Hz",
                "Add presence around 800 Hz - 2 kHz"
            ]
            tips["processing_tips"] = [
                "Use compression with slow attack for punch",
                "Consider multiband compression",
                "Ensure mono compatibility in low end"
            ]
        
        # Add confidence-based advice
        if confidence < 0.6:
            tips["mixing_advice"].append(f"Low confidence ({confidence:.2f}) - verify instrument identification")
        
        return tips
        
    except Exception as e:
        return {"error": f"Production tips generation failed: {str(e)}"}

async def _generate_frequency_profile(analysis: dict, instrument_type: str) -> dict:
    """Generate frequency profile for the instrument."""
    try:
        freq_bands = analysis.get("frequency_bands", {})
        spectral = analysis.get("spectral", {})
        
        profile = {
            "dominant_frequencies": [],
            "energy_distribution": {},
            "spectral_shape": {}
        }
        
        # Energy distribution
        total_energy = sum(freq_bands.values()) if freq_bands else 1
        if total_energy > 0:
            profile["energy_distribution"] = {
                "bass_20_200": (freq_bands.get("bass_energy", 0) / total_energy) * 100,
                "low_mid_200_800": (freq_bands.get("low_mid_energy", 0) / total_energy) * 100,
                "mid_800_3200": (freq_bands.get("mid_energy", 0) / total_energy) * 100,
                "high_mid_3200_8000": (freq_bands.get("high_mid_energy", 0) / total_energy) * 100,
                "high_8000_16000": (freq_bands.get("high_energy", 0) / total_energy) * 100
            }
        
        # Spectral shape
        profile["spectral_shape"] = {
            "centroid_hz": spectral.get("centroid_mean", 0),
            "bandwidth_hz": spectral.get("bandwidth_mean", 0),
            "rolloff_hz": spectral.get("rolloff_mean", 0)
        }
        
        # Instrument-specific dominant frequencies
        if instrument_type == "vocals":
            profile["dominant_frequencies"] = ["Formants: 300-3400 Hz", "Presence: 2-5 kHz"]
        elif instrument_type == "drums":
            profile["dominant_frequencies"] = ["Kick: 60-100 Hz", "Snare: 200 Hz & 2-4 kHz", "Cymbals: 8-16 kHz"]
        elif instrument_type == "bass":
            profile["dominant_frequencies"] = ["Fundamentals: 40-200 Hz", "Harmonics: 200-800 Hz"]
        
        return profile
        
    except Exception as e:
        return {"error": f"Frequency profile generation failed: {str(e)}"}

# =============================================================================
# VISUALIZATION TOOLS (PHASE 4)
# =============================================================================

@mcp.tool()
async def iara_visualizar_ondas_do_tempo(
    caminho_arquivo: str,
    mostrar_envelope: bool = True,
    normalizar: bool = True,
    caminho_saida: str = None
) -> dict:
    """
    Visualizar Ondas do Tempo - Gera gráfico waveform (forma de onda) temporal do áudio, mostrando amplitude ao longo do tempo com opções de envelope e normalização.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        mostrar_envelope: Se deve mostrar o envelope de amplitude
        normalizar: Se deve normalizar a amplitude
        caminho_saida: Caminho opcional para salvar o gráfico (None para base64)
    
    Returns:
        Waveform visualization as base64 image or file path
    """
    try:
        from .server_fastmcp import detectar_modo_visualizacao
        if caminho_saida is None:
            modo = detectar_modo_visualizacao()
            if modo == "local":
                caminho_saida = "/tmp/waveform.png"
            # If modo is 'remoto', keep caminho_saida as None to return base64

        if not Path(caminho_arquivo).exists():
            return {"error": f"File not found: {caminho_arquivo}"}
        
        result = await visualizer.create_waveform(
            file_path=caminho_arquivo,
            output_path=caminho_saida,
            show_envelope=mostrar_envelope,
            normalize=normalizar
        )
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Waveform visualization failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_criar_mapa_das_frequencias(
    caminho_arquivo: str,
    tipo_espectrograma: str = "stft",
    caminho_saida: str = None,
    tamanho_salto: int = 512,
    tamanho_fft: int = 2048
) -> dict:
    """
    Criar Mapa das Frequências - Gera espectrograma (STFT, Mel, CQT) mostrando distribuição de frequências ao longo do tempo, com parâmetros configuráveis de resolução.
    
    Args:
        caminho_arquivo: Caminho para o arquivo de áudio
        tipo_espectrograma: Tipo de espectrograma ('stft', 'mel', 'cqt')
        caminho_saida: Caminho opcional para salvar o gráfico (None para base64)
        tamanho_salto: Tamanho do salto para análise
        tamanho_fft: Tamanho da janela FFT
    
    Returns:
        Visualização do espectrograma como imagem base64 ou caminho do arquivo
    """
    try:
        import os
        from pathlib import Path
        # Importar detectar_modo_visualizacao apenas aqui para evitar erro de import global
        def _detectar_modo_visualizacao_fallback():
            try:
                from .server_fastmcp import detectar_modo_visualizacao
                return detectar_modo_visualizacao()
            except Exception:
                return "local"

        if not Path(caminho_arquivo).exists():
            return {"error": f"File not found: {caminho_arquivo}"}

        valid_types = ['stft', 'mel', 'cqt']
        if tipo_espectrograma not in valid_types:
            return {
                "error": f"Invalid spectrogram type: {tipo_espectrograma}",
                "valid_types": valid_types
            }

        # Fallback automático e montagem de caminho de saída completo
        modo = _detectar_modo_visualizacao_fallback()
        if caminho_saida:
            if os.path.isdir(caminho_saida) or caminho_saida.endswith(os.sep):
                output_path = os.path.join(caminho_saida, "spectrograma.png")
            else:
                output_path = caminho_saida
        else:
            output_path = "/tmp/spectrograma.png" if modo == "local" else None

        result = await visualizer.create_spectrogram(
            file_path=caminho_arquivo,
            output_path=output_path,
            spectrogram_type=tipo_espectrograma,
            hop_length=tamanho_salto,
            n_fft=tamanho_fft
        )
        return result
    except Exception as e:
        import traceback
        return {
            "error": f"Spectrogram visualization failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_pintar_essencia_musical(
    file_path: str,
    plot_type: str = "comprehensive",
    output_path: str = None
) -> dict:
    """
    Pintar Essência Musical - Gera gráficos de visualização das características extraídas (espectrograma, features temporais, harmônicos) em formato PNG.
    
    Args:
        file_path: Path to the audio file
        plot_type: Type of feature plot ('comprehensive', 'spectral', 'rhythmic')
        output_path: Optional path to save the plot (None for base64)
    
    Returns:
        Feature visualization as base64 image or file path
    """
    try:
        from .server_fastmcp import detectar_modo_visualizacao
        if output_path is None:
            modo = detectar_modo_visualizacao()
            if modo == "local":
                output_path = "/tmp/"
            # If modo is 'remoto', keep output_path as None

        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        # First extract features from the audio file
        analysis_result = await analyzer.analyze_complete(file_path)
        if "error" in analysis_result:
            return analysis_result
        
        features = analysis_result.get("analysis", {})

        output_file_path = None
        if output_path:
            output_filename = "essencia_musical.png"
            output_file_path = os.path.join(output_path, output_filename)

        result = await visualizer.create_feature_analysis_plot(
            features=features,
            output_path=output_file_path,
            plot_type=plot_type
        )
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Feature visualization failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_desenhar_correntes_separadas(
    file_path: str,
    separation_method: str = "htdemucs_ft",
    output_path: str = None
) -> dict:
    """
    Desenhar Correntes Separadas - Cria gráficos comparativos dos stems separados (waveforms, espectrogramas) para visualizar a qualidade da separação.
    
    Args:
        file_path: Path to the audio file
        separation_method: Demucs model to use for separation
        output_path: Optional path to save the plot (None for base64)
    
    Returns:
        Stems comparison visualization as base64 image or file path
    """
    try:
        from .server_fastmcp import detectar_modo_visualizacao
        if output_path is None:
            modo = detectar_modo_visualizacao()
            if modo == "local":
                output_path = "/tmp/"
            # If modo is 'remoto', keep output_path as None

        import os
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        # Perform source separation first
        separation_result = await separator.separate_audio(
            file_path=file_path,
            output_dir=None  # Use temp directory
        )
        
        if "error" in separation_result:
            return separation_result
        
        # Extract stem paths
        stems_data = {}
        separation_info = separation_result.get("separation", {})
        stems_info = separation_info.get("stems", {})
        
        for stem_name, stem_info in stems_info.items():
            stem_path = stem_info.get("path")
            if stem_path and Path(stem_path).exists():
                stems_data[stem_name] = stem_path
        
        if not stems_data:
            return {"error": "No valid stems found after separation"}
        
        # Compose full output file path if output_path is a directory
        output_file = None
        if output_path:
            # If output_path appears to be a directory, append filename
            if os.path.isdir(output_path) or output_path.endswith(os.sep):
                output_file = os.path.join(output_path, "stems_comparison.png")
            else:
                # If output_path is a file path, use as is
                output_file = output_path
        
        # Create visualization
        result = await visualizer.create_stems_comparison(
            stems_data=stems_data,
            output_path=output_file
        )
        
        # Cleanup temp files
        metadata = separation_result.get("metadata", {})
        if metadata.get("temporary_directory", False):
            output_dir = metadata.get("output_directory")
            if output_dir:
                separator.cleanup_temp_files(output_dir)
        
        return result
        
    except Exception as e:
        import traceback
        return {
            "error": f"Stems visualization failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_revelar_artes_visuais() -> dict:
    """
    Revelar Artes Visuais - Lista todos os tipos de gráficos e visualizações disponíveis no sistema, com descrições de cada tipo.
    
    Returns:
        Available plot types, descriptions, and system information
    """
    try:
        return {
            "visualization_available": VISUALIZATION_AVAILABLE,
            "supported_plot_types": AudioVisualizer.get_supported_plot_types(),
            "plot_descriptions": AudioVisualizer.get_plot_descriptions(),
            "output_formats": ["base64", "png", "jpg", "svg"],
            "spectrogram_types": ["stft", "mel", "cqt"],
            "feature_plot_types": ["comprehensive", "spectral", "rhythmic"],
            "recommendations": {
                "waveform": "Best for analyzing dynamics and overall structure",
                "stft_spectrogram": "General-purpose frequency analysis",
                "mel_spectrogram": "Perceptually motivated for music analysis", 
                "cqt_spectrogram": "Musical pitch representation",
                "feature_analysis": "Comprehensive overview of musical characteristics",
                "stems_comparison": "Compare separated instrument stems"
            }
        }
        
    except Exception as e:
        return {
            "visualization_available": VISUALIZATION_AVAILABLE,
            "error": f"Failed to get visualization info: {str(e)}"
        }

# =============================================================================
# OPTIMIZATION TOOLS (PHASE 4)
# =============================================================================

@mcp.tool()
def iara_mostrar_poder_das_aguas() -> dict:
    """
    Mostrar Poder das Águas - Exibe estatísticas detalhadas de performance do sistema (uso de memória, cache, tempo de processamento).
    
    Returns:
        Performance metrics, cache statistics, and optimization info
    """
    try:
        stats = optimizer.get_performance_stats()
        stats.update({
            "optimization_available": OPTIMIZATION_AVAILABLE,
            "system_info": {
                "cpu_count": os.cpu_count(),
                "max_workers": getattr(optimizer, 'max_workers', 'unknown')
            }
        })
        return stats
        
    except Exception as e:
        return {
            "optimization_available": OPTIMIZATION_AVAILABLE,
            "error": f"Failed to get performance stats: {str(e)}"
        }

@mcp.tool()
def iara_purificar_memorias() -> dict:
    """
    Purificar Memórias - Limpa todo o cache do sistema (análises, separações, visualizações) para liberar memória e garantir resultados atualizados.
    
    Returns:
        Status of cache clearing operation
    """
    try:
        optimizer.clear_cache()
        return {
            "success": True,
            "message": "Cache cleared successfully",
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        import traceback
        return {
            "error": f"Failed to clear cache: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
async def iara_harmonizar_fluxo_musical(
    file_path: str,
    operations: list = None,
    enable_parallel: bool = True
) -> dict:
    """
    Harmonizar Fluxo Musical - Executa workflow otimizado combinando múltiplas operações (análise + separação + classificação + visualização) de forma paralela e eficiente.
    
    Args:
        file_path: Path to the audio file
        operations: List of operations to perform ['analysis', 'separation', 'classification', 'visualization']
        enable_parallel: Whether to run operations in parallel when possible
    
    Returns:
        Results from all requested operations with performance metrics
    """
    try:
        if not Path(file_path).exists():
            return {"error": f"File not found: {file_path}"}
        
        if operations is None:
            operations = ['analysis', 'classification']
        
        start_time = time.time()
        results = {
            "file_path": file_path,
            "operations_requested": operations,
            "results": {},
            "performance": {}
        }
        
        # Define operation functions
        async def run_analysis():
            return await analyzer.analyze_complete(file_path)
        
        async def run_separation():
            return await separator.separate_audio(file_path)
        
        async def run_classification():  
            return await classifier.identify_instruments(file_path)
        
        async def run_visualization():
            return await visualizer.create_waveform(file_path)
        
        operation_map = {
            'analysis': ('analysis', run_analysis, (), {}),
            'separation': ('separation', run_separation, (), {}),
            'classification': ('classification', run_classification, (), {}),
            'visualization': ('visualization', run_visualization, (), {})
        }
        
        # Filter valid operations
        valid_operations = [
            operation_map[op] for op in operations 
            if op in operation_map
        ]
        
        if not valid_operations:
            return {
                "error": "No valid operations specified",
                "available_operations": list(operation_map.keys())
            }
        
        # Run operations
        if enable_parallel and len(valid_operations) > 1:
            # Run in parallel
            operation_results = await optimizer.run_parallel(valid_operations)
            
            # Map results back to operation names
            for i, op_name in enumerate([op[0] for op in valid_operations]):
                results["results"][op_name] = operation_results[i]
        else:
            # Run sequentially with caching
            for op_name, func, args, kwargs in valid_operations:
                op_start = time.time()
                result = await optimizer.run_with_cache(
                    op_name, func, file_path, *args, **kwargs
                )
                results["results"][op_name] = result
                results["performance"][f"{op_name}_time"] = time.time() - op_start
        
        # Overall performance
        total_time = time.time() - start_time
        results["performance"]["total_time_seconds"] = total_time
        results["performance"]["parallel_enabled"] = enable_parallel
        
        return results
        
    except Exception as e:
        import traceback
        return {
            "error": f"Optimized workflow failed: {str(e)}",
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def iara_compartilhar_sabedoria_otimizacao() -> dict:
    """
    Compartilhar Sabedoria de Otimização - Fornece informações sobre recursos de otimização, configurações de cache e recomendações de performance.
    
    Returns:
        Optimization features, cache info, and performance recommendations
    """
    try:
        return {
            "optimization_available": OPTIMIZATION_AVAILABLE,
            "features": {
                "caching": "LRU cache with file change detection",
                "parallel_processing": "Multi-threaded execution",
                "memory_optimization": "Chunk-based processing for large files",
                "batch_processing": "Efficient handling of multiple files"
            },
            "cache_info": optimizer.cache.get_stats() if OPTIMIZATION_AVAILABLE else {},
            "recommendations": {
                "small_files": "Use caching for repeated analysis",
                "large_files": "Enable chunk-based processing",
                "batch_jobs": "Use parallel processing for multiple files",
                "memory_limited": "Clear cache periodically"
            },
            "performance_tips": [
                "Enable caching for repeated operations on same files",
                "Use parallel processing for independent operations",
                "Clear cache when analyzing many different files",
                "Use appropriate chunk sizes for large audio files"
            ]
        }
        
    except Exception as e:
        return {
            "optimization_available": OPTIMIZATION_AVAILABLE,
            "error": f"Failed to get optimization info: {str(e)}"
        }

if __name__ == "__main__":
    # Para Claude Desktop, usar FastMCP diretamente
    mcp.run()