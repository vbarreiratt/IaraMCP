# 🧜‍♀️ IaraMCP - Servidor de Análise Musical das Águas

*Inspirado na Iara, ser mitológico brasileiro das águas, que seduz com sua música encantadora*

IaraMCP é um servidor MCP (Model Context Protocol) que combina a sabedoria ancestral da Iara com tecnologias modernas de análise musical. Como a sereia dos rios brasileiros, este servidor desvenda os segredos sonoros que fluem nas correntes musicais.

## 🌊 A Lenda da Iara Musical

Na mitologia brasileira, a Iara é uma sereia que habita rios e lagos, conhecida por sua voz hipnotizante e conhecimento profundo das águas. IaraMCP incorpora essa essência, mergulhando nas profundezas dos arquivos de áudio para revelar seus mistérios musicais mais ocultos.

## ✨ Poderes da Iara (Ferramentas Disponíveis)

### 🔮 **Ferramentas Essenciais**
- **`iara_despertar`** - Desperta a Iara e verifica seus poderes
- **`iara_validar_cristais_sonoros`** - Valida arquivos de áudio (MP3, WAV, FLAC, M4A, OGG)
- **`iara_mergulhar_nas_ondas`** - Análise musical completa (tempo, harmonia, espectro, ritmo)

### 🌀 **Separação das Correntes**
- **`iara_separar_correntes_musicais`** - Separa áudio em stems (vocals, drums, bass, other)
- **`iara_examinar_corrente_isolada`** - Analisa stems individuais em detalhes
- **`iara_comparar_magias_separadoras`** - Compara diferentes modelos de separação

### 🎭 **Reconhecimento dos Espíritos Musicais**
- **`iara_reconhecer_instrumentos_das_aguas`** - Detecta instrumentos com ML
- **`iara_identificar_voz_das_aguas`** - Classifica stems por tipo de instrumento
- **`iara_revelar_alma_do_instrumento`** - Perfil detalhado de instrumentos

### 🎨 **Artes Visuais das Águas**
- **`iara_visualizar_ondas_do_tempo`** - Gera waveforms temporais
- **`iara_criar_mapa_das_frequencias`** - Cria espectrogramas (STFT, Mel, CQT)
- **`iara_pintar_essencia_musical`** - Visualizações de características musicais
- **`iara_desenhar_correntes_separadas`** - Gráficos comparativos de stems

### 📊 **Sabedoria Ancestral**
- **`iara_tecer_relatorio_das_aguas`** - Relatórios completos formatados
- **`iara_explorar_caverna_sonora`** - Análise em lote de diretórios
- **`iara_harmonizar_fluxo_musical`** - Workflow otimizado completo

### ⚡ **Poder das Águas (Otimização)**
- **`iara_mostrar_poder_das_aguas`** - Estatísticas de performance
- **`iara_purificar_memorias`** - Limpeza de cache
- **`iara_compartilhar_sabedoria_otimizacao`** - Informações de otimização

## 🚀 Invocando a Iara (Instalação)

### 1. Preparar as Águas
```bash
pip install -r requirements.txt
```

### 2. Despertar a Iara
```bash
python test_basic.py
```

### 3. Conectar ao Claude Desktop
Adicione ao `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "iaramcp": {
      "command": "/opt/anaconda3/bin/python",
      "args": ["-m", "iaramcp.server_fastmcp"],
      "env": {"PYTHONPATH": "/Users/vitor/Desktop/IaraMCP/src"}
    }
  }
}
```

## 🎵 Exemplo de Poder da Iara

Quando a Iara analisa "NA ONDA DA BABYLON.m4a":
- **Duração das Águas**: 2:31.1
- **Batida do Coração**: 136.0 BPM  
- **Tom da Sereia**: E
- **Tempo de Mergulho**: ~15 segundos

## 🏛️ Templo da Iara (Estrutura do Projeto)

```
src/iaramcp/
├── server_fastmcp.py      # 🧜‍♀️ Servidor principal da Iara
├── audio/
│   ├── analysis.py        # 🔍 Análise das correntes sonoras
│   ├── separation.py      # 🌊 Separação das águas musicais
│   └── utils.py          # 🛠️ Utilitários mágicos
├── ml/
│   └── classifier.py     # 🎭 Classificação de espíritos musicais
├── visualization/
│   └── plots.py          # 🎨 Arte visual das águas
└── optimization/
    └── performance.py    # ⚡ Poder e otimização
```

## 🌟 Lenda Realizada (Critérios de Sucesso)

- ✅ A Iara desperta sem erros
- ✅ Analisa arquivos musicais via Claude Desktop
- ✅ Domina formatos M4A, MP3, WAV, FLAC, OGG
- ✅ Revela segredos musicais detalhados
- ✅ Protege das tempestades (tratamento de erros)
- ✅ Separa correntes musicais com Demucs
- ✅ Reconhece instrumentos com sabedoria ancestral
- ✅ Cria visualizações encantadoras

## 🔮 Evolução dos Poderes

### 🌊 Águas Atuais (Implementado)
- Análise musical completa com librosa
- Separação de fontes com Demucs (htdemucs_ft)
- Classificação heurística de instrumentos
- Visualizações spectograficas e temporais
- Cache inteligente e otimizações

### 🌙 Águas Futuras (Próximas Versões)
- Modelos ML personalizados para instrumentos brasileiros
- Detecção de gêneros musicais brasileiros
- Análise de harmonia complexa
- Exportação para formatos de partitura

## 💎 Cristais Mágicos (Dependências)

- `mcp>=1.0.0` - Protocolo das águas encantadas
- `fastmcp` - Velocidade dos rios
- `librosa>=0.10.0` - Sabedoria da análise sonora
- `demucs>=4.0.0` - Magia da separação de fontes
- `torch>=2.0.0` - Poder do aprendizado profundo
- `numpy>=1.21.0` - Matemática das correntes
- `matplotlib>=3.5.0` - Pincéis das visualizações

---

🧜‍♀️ *"Nas águas dos rios brasileiros, a Iara canta seus segredos musicais. IaraMCP é sua voz digital, revelando os mistérios sonoros que ecoam nas profundezas da música."*