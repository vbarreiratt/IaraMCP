# 🧜‍♀️ IaraMCP - Servidor de Análise Musical das Águas

*Inspirado na Iara, ser mitológico brasileiro das águas, que seduz com sua música encantadora*

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![MCP Protocol](https://img.shields.io/badge/protocol-MCP-green.svg)](https://modelcontextprotocol.io)
[![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)]()

IaraMCP é um servidor MCP (Model Context Protocol) que combina a sabedoria ancestral da Iara com tecnologias modernas de análise musical. Como a sereia dos rios brasileiros, este servidor desvenda os segredos sonoros que fluem nas correntes musicais.

## 🌊 A Lenda da Iara Musical

Na mitologia brasileira, a Iara é uma sereia que habita rios e lagos, conhecida por sua voz hipnotizante e conhecimento profundo das águas. IaraMCP incorpora essa essência, mergulhando nas profundezas dos arquivos de áudio para revelar seus mistérios musicais mais ocultos.

## ✨ Poderes da Iara (22 Ferramentas Disponíveis)

### 🔮 **Análise e Validação**
- **`iara_despertar`** - Desperta a Iara e verifica todos os módulos
- **`iara_validar_cristais_sonoros`** - Valida arquivos de áudio (MP3, WAV, FLAC, M4A, OGG)
- **`iara_mergulhar_nas_ondas`** - Análise musical completa (tempo, harmonia, espectro, ritmo)
- **`iara_tecer_relatorio_das_aguas`** - Relatórios completos formatados (JSON/texto)
- **`iara_explorar_caverna_sonora`** - Análise em lote de diretórios

### 🌀 **Separação de Fontes (Demucs)**
- **`iara_separar_correntes_musicais`** - Separa áudio em stems (vocals, drums, bass, other)
- **`iara_examinar_corrente_isolada`** - Analisa stems individuais em detalhes
- **`iara_comparar_magias_separadoras`** - Compara modelos de separação (htdemucs_ft, htdemucs)
- **`iara_revelar_segredos_separacao`** - Lista modelos e configurações disponíveis

### 🎭 **Classificação de Instrumentos**
- **`iara_reconhecer_instrumentos_das_aguas`** - Detecta instrumentos com análise espectral e ML
- **`iara_identificar_voz_das_aguas`** - Classifica stems por tipo de instrumento
- **`iara_revelar_alma_do_instrumento`** - Perfil detalhado com características tímbricas
- **`iara_mostrar_sabedoria_classificadora`** - Lista instrumentos suportados e métodos

### 🎨 **Visualizações Encantadas**
- **`iara_visualizar_ondas_do_tempo`** - Gera waveforms temporais com envelope
- **`iara_criar_mapa_das_frequencias`** - Cria espectrogramas (STFT, Mel, CQT)
- **`iara_pintar_essencia_musical`** - Visualizações de características musicais
- **`iara_desenhar_correntes_separadas`** - Gráficos comparativos de stems
- **`iara_revelar_artes_visuais`** - Lista tipos de visualizações disponíveis

### ⚡ **Otimização e Performance**
- **`iara_mostrar_poder_das_aguas`** - Estatísticas detalhadas de performance
- **`iara_purificar_memorias`** - Limpeza de cache para liberar memória
- **`iara_harmonizar_fluxo_musical`** - Workflow otimizado paralelo completo
- **`iara_compartilhar_sabedoria_otimizacao`** - Informações de otimização e cache

## 🚀 Invocando a Iara (Instalação)

### Requisitos Básicos
- Python 3.8+
- macOS, Linux ou Windows
- ffmpeg (para processamento de áudio)

### 1. Instalação via pip
```bash
git clone <repository-url>
cd IaraMCP
pip install -e .
```

### 2. Instalação com dependências avançadas
```bash
pip install -e .[advanced]
```

### 3. Configuração do Claude Desktop
Adicione ao `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iaramcp": {
      "command": "python",
      "args": ["-m", "iaramcp.server_fastmcp"],
      "env": {
        "PYTHONPATH": "/caminho/para/IaraMCP/src"
      }
    }
  }
}
```

### 4. Testando a Conexão
```bash
# Via Claude Desktop - use a ferramenta:
iara_despertar("Olá, Iara!")
```

## 🎵 Compatibilidade e Fallback

IaraMCP foi projetado para funcionar tanto **localmente** (Claude Desktop, MCP Inspector) quanto **remotamente** (Smithery.ai, serviços em nuvem):

- **Local**: Salva arquivos de visualização no desktop
- **Remoto**: Retorna imagens como base64 ou dados processáveis
- **Fallback automático**: Detecta o ambiente e ajusta o comportamento

## 🏛️ Arquitetura do Templo da Iara

```
IaraMCP/
├── src/iaramcp/
│   ├── server_fastmcp.py      # 🧜‍♀️ Servidor principal da Iara
│   ├── audio/
│   │   ├── analysis.py        # 🔍 Análise das correntes sonoras
│   │   ├── separation.py      # 🌊 Separação das águas musicais
│   │   └── utils.py          # 🛠️ Utilitários mágicos
│   ├── ml/
│   │   └── classifier.py     # 🎭 Classificação de espíritos musicais
│   ├── visualization/
│   │   └── plots.py          # 🎨 Arte visual das águas
│   └── optimization/
│       └── performance.py    # ⚡ Poder e otimização
├── README.md                  # 📖 Este guia
├── pyproject.toml            # 📦 Configuração do projeto
├── Dockerfile                # 🐳 Container para nuvem
├── smithery.yaml             # ☁️ Configuração Smithery.ai
└── requirements.txt          # 📋 Dependências
```

## 🎯 Casos de Uso Principais

### Análise Musical Completa
```python
# Via Claude Desktop
iara_mergulhar_nas_ondas("/caminho/para/musica.mp3", "completa")
```

### Separação de Instrumentos
```python
# Separar em stems individuais
iara_separar_correntes_musicais("/caminho/para/musica.mp3", "demucs", "htdemucs_ft")
```

### Workflow Otimizado
```python
# Análise + classificação + visualização em paralelo
iara_harmonizar_fluxo_musical("/caminho/para/musica.mp3", 
                             ["analysis", "classification", "visualization"])
```

## 🌟 Lenda Realizada (Status de Produção)

- ✅ **22 ferramentas** temáticas funcionais
- ✅ **Compatibilidade cross-platform** (local/remoto)
- ✅ **Sistema de fallback** automático robusto
- ✅ **Análise musical** completa com librosa
- ✅ **Separação de fontes** com Demucs (5+ modelos)
- ✅ **Classificação de instrumentos** heurística e ML
- ✅ **Visualizações** (waveform, spectrograms, features)
- ✅ **Cache inteligente** e otimizações de performance
- ✅ **Tratamento de erros** robusto
- ✅ **Suporte a formatos**: M4A, MP3, WAV, FLAC, OGG
- ✅ **Pronto para Smithery.ai** deployment

## 💎 Tecnologias Utilizadas

### Core
- **MCP Protocol** - Comunicação com Claude
- **FastMCP** - Framework ágil para MCP servers
- **FastAPI** - API web moderna para health checks

### Audio Processing
- **librosa** - Análise musical e extração de features
- **Demucs** - Separação de fontes estado-da-arte
- **soundfile** - I/O de arquivos de áudio

### Machine Learning
- **PyTorch** - Deep learning para Demucs
- **scikit-learn** - Classificação de instrumentos
- **numpy/scipy** - Computação científica

### Visualization
- **matplotlib** - Visualizações e gráficos
- **seaborn** - Gráficos estatísticos elegantes

## 🔮 Roadmap Futuro

### v0.2.0 - Águas Brasileiras
- Detecção de gêneros musicais brasileiros
- Instrumentos tradicionais (berimbau, cuíca, pandeiro)
- Análise rítmica específica (samba, bossa nova, forró)

### v0.3.0 - Águas Profundas  
- Modelos ML personalizados
- Análise harmônica avançada
- Exportação para MIDI/MusicXML

## 📄 Licença

MIT License - Livre como as águas dos rios brasileiros

---

🧜‍♀️ *"Nas águas dos rios brasileiros, a Iara canta seus segredos musicais. IaraMCP é sua voz digital, revelando os mistérios sonoros que ecoam nas profundezas da música moderna."*

**Criado com 💙 inspirado na rica mitologia brasileira**