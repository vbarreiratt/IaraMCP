# 🧜‍♀️ IaraMCP - Especificações dos Poderes da Sereia Musical

## 🌊 MISSÃO ANCESTRAL DA IARA
Materializar digitalmente os poderes da Iara, ser mitológico brasileiro das águas, através de um servidor MCP que combina sabedoria ancestral com tecnologias modernas de análise musical. A Iara mergulhará nas correntes sonoras para revelar segredos musicais ocultos nas profundezas dos arquivos de áudio.

## 🎯 FUNCIONALIDADES CORE REQUERIDAS

### 1. **Separação de Fontes Sonoras**
- Integrar **Demucs** (v4 - Hybrid Transformer) para separação de alta qualidade
- Separar áudio em stems: vocals, drums, bass, other/accompaniment
- Suporte a múltiplos modelos: `htdemucs_ft`, `htdemucs`, `hdemucs_mmi`
- Output em formatos: WAV, MP3, FLAC

### 2. **Identificação de Instrumentos**
- Detectar instrumentos usando stems separados para maior precisão
- Classificar: vocals, drums, bass, guitar, piano, strings, brass, woodwinds, synth
- Sistema de confiança (confidence score) para cada detecção
- Análise heurística baseada em características espectrais

### 3. **Análise Musical Completa**
- **Temporal**: BPM, beat tracking, tempo changes
- **Harmônica**: chroma features, key detection, chord progression
- **Espectral**: MFCC, spectral centroid, bandwidth, rolloff
- **Rítmica**: onset detection, rhythm patterns
- **Energia**: RMS, dynamic range, loudness

### 4. **Ferramentas MCP Específicas**
```
1. separate_audio_sources(file_path, method="demucs", model="htdemucs_ft")
2. identify_instruments(file_path, use_separation=True, confidence_threshold=0.7)
3. analyze_musical_features(file_path, analysis_type="complete")
4. generate_music_report(file_path, format="json", include_visualizations=True)
5. compare_separation_methods(file_path, methods=["demucs"], metrics=["quality"])
6. analyze_individual_stem(stem_path, instrument_type="auto")
7. batch_analyze_directory(directory_path, file_extensions=[".mp3", ".wav", ".m4a"])
```

## 🛠️ STACK TECNOLÓGICO OBRIGATÓRIO

### **Core Dependencies**
```python
mcp >= 1.0.0                    # Model Context Protocol
librosa >= 0.10.0              # Audio analysis
demucs >= 4.0.0                # Source separation (Facebook Research)
torch >= 2.0.0                 # PyTorch for Demucs
torchaudio >= 2.0.0            # Audio processing
numpy >= 1.21.0                # Numerical computing
scipy >= 1.7.0                 # Scientific computing
soundfile >= 0.12.0            # Audio file I/O
```

### **Optional Advanced Features**
```python
scikit-learn >= 1.0.0          # ML for instrument classification
matplotlib >= 3.5.0            # Visualizations
essentia >= 2.1b6.dev858       # Advanced audio analysis
madmom >= 0.16.1               # Music information retrieval
```

## 📁 ESTRUTURA DE PROJETO REQUERIDA

```
mcp-advanced-music/
├── pyproject.toml              # Project configuration
├── README.md                   # Documentation
├── .gitignore                  # Git ignore
├── requirements.txt            # Dependencies
└── src/
    └── iaramcp/
        ├── __init__.py         # Package init
        ├── server.py           # Main MCP server
        ├── audio/
        │   ├── __init__.py
        │   ├── separation.py   # Demucs integration
        │   ├── analysis.py     # Librosa analysis
        │   └── utils.py        # Audio utilities
        ├── ml/
        │   ├── __init__.py
        │   ├── classifier.py   # Instrument classification
        │   └── features.py     # Feature extraction
        ├── visualization/
        │   ├── __init__.py
        │   └── plots.py        # Audio visualizations
        └── tools/
            ├── __init__.py
            └── mcp_tools.py    # MCP tool definitions
```

## 🎼 CASOS DE USO ESPECÍFICOS

### **Caso de Uso Principal**
```
INPUT: /Users/vitor/Desktop/NA ONDA DA BABYLON.m4a
EXPECTED OUTPUT:
{
  "file_info": {...},
  "separation": {
    "method": "demucs",
    "model": "htdemucs_ft", 
    "stems": {
      "vocals": {"path": "...", "confidence": 0.95},
      "drums": {"path": "...", "confidence": 0.92},
      "bass": {"path": "...", "confidence": 0.87},
      "other": {"path": "...", "confidence": 0.83}
    }
  },
  "instruments_detected": [
    {"type": "vocals", "subtype": "rap_vocals", "confidence": 0.95},
    {"type": "drums", "subtype": "trap_kit", "confidence": 0.92},
    {"type": "bass", "subtype": "808_bass", "confidence": 0.87},
    {"type": "synth", "subtype": "lead_synth", "confidence": 0.83}
  ],
  "musical_analysis": {
    "tempo_bpm": 136,
    "key": "C minor",
    "time_signature": "4/4",
    "duration": 143.27,
    "energy_level": "high",
    "genre_prediction": "trap/hip-hop"
  }
}
```

## 🔧 REQUISITOS TÉCNICOS ESPECÍFICOS

### **MCP Server Implementation**
- Use `mcp.server.Server` class
- Implement proper `stdio_server` communication
- Handle errors gracefully with meaningful messages
- Support async operations for heavy processing
- Include progress callbacks for long operations

### **Audio Processing Requirements**
- Support formats: MP3, WAV, FLAC, M4A, OGG
- Handle mono and stereo audio
- Automatic sample rate conversion
- Memory-efficient processing for large files
- Temporary file management with cleanup

### **Performance Optimization**
- Use multiprocessing for CPU-intensive tasks
- Implement caching for repeated analyses
- Batch processing capabilities
- GPU acceleration when available (CUDA)
- Streaming analysis for very large files

### **Error Handling & Validation**
- Validate audio file formats before processing
- Handle corrupted audio files gracefully
- Provide meaningful error messages
- File size and duration limits
- Memory usage monitoring

## 🧪 TESTING REQUIREMENTS

### **Test Cases to Include**
```python
def test_cases():
    # Basic functionality
    test_audio_file_loading()
    test_demucs_separation()
    test_instrument_detection()
    test_musical_analysis()
    
    # Edge cases
    test_corrupted_audio_file()
    test_very_short_audio()
    test_very_long_audio()
    test_mono_vs_stereo()
    test_different_sample_rates()
    
    # Integration tests
    test_full_pipeline()
    test_mcp_communication()
```

## 📊 OUTPUT FORMATS

### **JSON Schema for Results**
```json
{
  "metadata": {
    "file_path": "string",
    "processing_time": "number",
    "timestamp": "ISO string"
  },
  "separation": {
    "method": "string",
    "quality_metrics": {...},
    "stems": {...}
  },
  "instruments": [...],
  "analysis": {
    "temporal": {...},
    "spectral": {...},
    "harmonic": {...}
  }
}
```

## 🚀 DEPLOYMENT CONFIGURATION

### **Claude Desktop Integration**
```json
{
  "mcpServers": {
    "advanced-music-analysis": {
      "command": "python",
      "args": ["-m", "iaramcp.server"],
      "env": {"PYTHONPATH": "..."}
    }
  }
}
```

## 💡 IMPLEMENTATION PRIORITIES

1. **FASE 1 (Core)**: Basic MCP server + Librosa analysis
2. **FASE 2 (Advanced)**: Demucs integration + Separation
3. **FASE 3 (ML)**: Instrument classification + Detection
4. **FASE 4 (Polish)**: Visualizations + Optimization

## 🎯 SUCCESS CRITERIA

- [ ] MCP server starts without errors
- [ ] Successfully analyzes audio files via Claude Desktop
- [ ] Separates "NA ONDA DA BABYLON.m4a" into identifiable stems
- [ ] Detects instruments with >80% accuracy
- [ ] Processes files under 10MB in <60 seconds
- [ ] Handles errors gracefully
- [ ] Provides detailed, actionable results

## 📝 ADDITIONAL CONTEXT

**Target User**: Music producer/analyst using Claude Desktop for audio analysis
**Primary Use Case**: Analyze existing songs to understand composition and production techniques
**Performance Target**: Real-time analysis for files under 5 minutes
**Quality Target**: Professional-grade separation and analysis results

---

**IMPORTANTE**: Implemente o servidor de forma incremental, testando cada componente antes de adicionar complexidade. Comece com funcionalidade básica e evolua gradualmente para features avançadas.

# ARQUIVO DE TESTE ESPECÍFICO
/Users/vitor/Desktop/NA ONDA DA BABYLON.m4a

# AMBIENTE ATUAL
- Python 3.12 (Anaconda)
- macOS
- Diretório: /Users/vitor/Desktop/mcp-advanced-music/
- Virtual env: .venv (já criado)

# COMEÇAR AGORA COM
1. Servidor MCP básico funcional
2. Teste com o arquivo específico
3. Depois evoluir para funcionalidades avançadas