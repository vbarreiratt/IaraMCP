# 🧜‍♀️ MANUAL.md - Guia Completo de Uso do IaraMCP

*Manual definitivo para usar todas as 22 ferramentas da Iara, com exemplos práticos e casos de uso*

## 🌊 Introdução ao Mundo da Iara

Este manual ensina como usar cada uma das 22 ferramentas temáticas do IaraMCP. A Iara, sereia brasileira das águas, empresta sua sabedoria para revelar os segredos musicais mais profundos.

### Convenções deste Manual
- **Arquivo de exemplo**: Vamos usar `"musica.mp3"` nos exemplos
- **Paths**: Substitua pelos caminhos reais dos seus arquivos
- **Claude Desktop**: Execute os comandos diretamente na interface
- **Resultados**: Todos retornam dados JSON estruturados

---

## 🔮 Ferramentas de Análise e Validação

### 1. `iara_despertar` - Despertar da Iara

**O que faz**: Testa a conexão e verifica o status de todos os módulos.

**Uso básico**:
```python
iara_despertar("Olá, Iara!")
```

**Exemplo de resultado**:
```json
"🧜‍♀️ IaraMCP está despertando das águas musicais! Análise: ✅ Fluindo, Separação: ✅ Fluindo, Classificação: ✅ Fluindo, Visualização: ✅ Fluindo, Otimização: ✅ Fluindo. Mensagem: Olá, Iara!"
```

**Quando usar**: Primeiro comando para verificar se tudo está funcionando.

---

### 2. `iara_validar_cristais_sonoros` - Validação de Arquivos

**O que faz**: Verifica se um arquivo de áudio é válido e extrai metadados básicos.

**Uso básico**:
```python
iara_validar_cristais_sonoros("/Users/vitor/Desktop/musica.mp3")
```

**Parâmetros**:
- `caminho_arquivo`: Caminho completo para o arquivo

**Exemplo de resultado**:
```json
{
  "caminho_arquivo": "/Users/vitor/Desktop/musica.mp3",
  "validacao": {
    "valid": true,
    "format": "mp3",
    "duration": 151.0
  },
  "info_arquivo": {
    "sample_rate": 44100,
    "channels": 2,
    "bitrate": 320
  },
  "timestamp": "2025-08-06 15:30:45"
}
```

**Formatos suportados**: MP3, WAV, FLAC, M4A, OGG

---

### 3. `iara_mergulhar_nas_ondas` - Análise Musical Completa

**O que faz**: Executa análise completa de características musicais (tempo, harmonia, espectro, ritmo).

**Uso básico**:
```python
# Análise completa
iara_mergulhar_nas_ondas("/Users/vitor/Desktop/musica.mp3", "completa")

# Análise básica (mais rápida)
iara_mergulhar_nas_ondas("/Users/vitor/Desktop/musica.mp3", "basica")
```

**Parâmetros**:
- `caminho_arquivo`: Caminho para o arquivo de áudio
- `tipo_analise`: `"basica"` ou `"completa"` (padrão)

**Exemplo de resultado (resumido)**:
```json
{
  "metadata": {
    "duration": 151.0,
    "sample_rate": 44100,
    "channels": 2
  },
  "analysis": {
    "temporal": {
      "tempo_bpm": 120.5,
      "beat_times": [0.5, 1.0, 1.5],
      "onset_rate_per_second": 2.3
    },
    "spectral": {
      "rms_energy": {"mean": 0.087},
      "spectral_centroid": {"mean": 1850.4},
      "spectral_bandwidth": {"mean": 2100.2}
    },
    "harmonic": {
      "estimated_key": "C",
      "key_confidence": 0.85,
      "harmonic_energy": 0.67
    },
    "rhythmic": {
      "tempo_stability": 0.92,
      "rhythm_complexity": 0.34
    }
  }
}
```

**Quando usar**: Para análise detalhada de qualquer música antes de outras operações.

---

### 4. `iara_tecer_relatorio_das_aguas` - Relatórios Formatados

**O que faz**: Gera relatório completo e formatado com análise musical detalhada.

**Uso básico**:
```python
# Relatório JSON
iara_tecer_relatorio_das_aguas("/Users/vitor/Desktop/musica.mp3", "json", False)

# Relatório com visualizações
iara_tecer_relatorio_das_aguas("/Users/vitor/Desktop/musica.mp3", "json", True)
```

**Parâmetros**:
- `file_path`: Caminho para o arquivo
- `format`: `"json"` ou `"text"`
- `include_visualizations`: `true` ou `false`

**Quando usar**: Para obter um relatório profissional completo da música.

---

### 5. `iara_explorar_caverna_sonora` - Análise em Lote

**O que faz**: Processa múltiplos arquivos de áudio em um diretório.

**Uso básico**:
```python
iara_explorar_caverna_sonora("/Users/vitor/Desktop/musicas/", [".mp3", ".wav", ".m4a"])
```

**Parâmetros**:
- `directory_path`: Caminho para o diretório
- `file_extensions`: Lista de extensões a processar

**Quando usar**: Para analisar uma biblioteca musical inteira.

---

## 🌀 Ferramentas de Separação de Fontes

### 6. `iara_separar_correntes_musicais` - Separação com Demucs

**O que faz**: Separa áudio em stems isolados (vocals, drums, bass, other) usando modelos Demucs.

**Uso básico**:
```python
# Separação com modelo padrão
iara_separar_correntes_musicais("/Users/vitor/Desktop/musica.mp3", "demucs", "htdemucs_ft", "wav", None)

# Especificando diretório de saída
iara_separar_correntes_musicais("/Users/vitor/Desktop/musica.mp3", "demucs", "htdemucs_ft", "wav", "/Users/vitor/Desktop/stems/")
```

**Parâmetros**:
- `caminho_arquivo`: Arquivo a separar
- `metodo`: `"demucs"` (único suportado)
- `modelo`: `"htdemucs_ft"`, `"htdemucs"`, `"mdx"`, etc.
- `formato_saida`: `"wav"`, `"mp3"`, `"flac"`
- `diretorio_saida`: Onde salvar (None para automático)

**Modelos disponíveis**:
- `htdemucs_ft`: Melhor qualidade (recomendado)
- `htdemucs`: Balanceado
- `mdx`: Mais rápido
- `mdx_extra`: Focado em vocals

**Exemplo de resultado**:
```json
{
  "separation": {
    "stems": {
      "vocals": {"path": "/path/to/vocals.wav", "confidence": 0.89},
      "drums": {"path": "/path/to/drums.wav", "confidence": 0.92},
      "bass": {"path": "/path/to/bass.wav", "confidence": 0.85},
      "other": {"path": "/path/to/other.wav", "confidence": 0.78}
    },
    "quality_metrics": {
      "overall_quality": 0.86,
      "processing_time": 45.2
    }
  }
}
```

**Quando usar**: Para isolar instrumentos específicos ou fazer remixes.

---

### 7. `iara_examinar_corrente_isolada` - Análise de Stems

**O que faz**: Analisa em detalhes um stem individual já separado.

**Uso básico**:
```python
iara_examinar_corrente_isolada("/Users/vitor/Desktop/stems/vocals.wav", "vocals")
```

**Parâmetros**:
- `stem_path`: Caminho para o arquivo stem
- `instrument_type`: `"vocals"`, `"drums"`, `"bass"`, `"other"`, ou `"auto"`

**Quando usar**: Após separação, para analisar qualidade e características de cada instrumento.

---

### 8. `iara_comparar_magias_separadoras` - Comparação de Modelos

**O que faz**: Testa múltiplos modelos de separação no mesmo arquivo e compara resultados.

**Uso básico**:
```python
iara_comparar_magias_separadoras("/Users/vitor/Desktop/musica.mp3", ["htdemucs_ft", "htdemucs", "mdx"], ["quality", "speed"])
```

**Parâmetros**:
- `file_path`: Arquivo a testar
- `methods`: Lista de modelos para comparar
- `metrics`: Métricas a avaliar

**Quando usar**: Para escolher o melhor modelo para seu tipo de música.

---

### 9. `iara_revelar_segredos_separacao` - Informações do Sistema

**O que faz**: Lista modelos disponíveis, formatos suportados e configurações do sistema.

**Uso básico**:
```python
iara_revelar_segredos_separacao()
```

**Exemplo de resultado**:
```json
{
  "separation_available": true,
  "available_models": {
    "htdemucs_ft": "High quality fine-tuned",
    "htdemucs": "Standard quality",
    "mdx": "Fast processing"
  },
  "device_info": {
    "cuda_available": false,
    "mps_available": true,
    "recommended_device": "mps"
  },
  "recommendations": {
    "best_quality": "htdemucs_ft",
    "fastest": "mdx"
  }
}
```

**Quando usar**: Para verificar capacidades do sistema antes de processar.

---

## 🎭 Ferramentas de Classificação de Instrumentos

### 10. `iara_reconhecer_instrumentos_das_aguas` - Detecção de Instrumentos

**O que faz**: Detecta e classifica instrumentos musicais presentes no áudio.

**Uso básico**:
```python
# Detecção básica
iara_reconhecer_instrumentos_das_aguas("/Users/vitor/Desktop/musica.mp3", True, 0.7, "heuristico")

# Com separação para maior precisão
iara_reconhecer_instrumentos_das_aguas("/Users/vitor/Desktop/musica.mp3", True, 0.8, "hibrido")
```

**Parâmetros**:
- `caminho_arquivo`: Arquivo a analisar
- `usar_separacao`: `true` para maior precisão (usa stems)
- `limiar_confianca`: Confiança mínima (0.0-1.0)
- `metodo`: `"heuristico"`, `"ml"`, `"hibrido"`

**Exemplo de resultado**:
```json
{
  "detected_instruments": [
    {"type": "vocals", "subtype": "male", "confidence": 0.92, "time_presence": "0-151s"},
    {"type": "drums", "subtype": "acoustic_kit", "confidence": 0.89, "time_presence": "5-151s"},
    {"type": "bass", "subtype": "electric", "confidence": 0.78, "time_presence": "8-151s"},
    {"type": "guitar", "subtype": "electric", "confidence": 0.85, "time_presence": "12-151s"}
  ],
  "analysis_metadata": {
    "method": "heuristic",
    "processing_time": 12.3,
    "used_separation": true
  }
}
```

**Quando usar**: Para catalogar automaticamente sua biblioteca musical.

---

### 11. `iara_identificar_voz_das_aguas` - Classificação de Stems

**O que faz**: Classifica automaticamente o tipo de instrumento em um stem separado.

**Uso básico**:
```python
iara_identificar_voz_das_aguas("/Users/vitor/Desktop/stems/vocals.wav", "vocals")
```

**Quando usar**: Para validar se a separação funcionou corretamente.

---

### 12. `iara_revelar_alma_do_instrumento` - Perfil Detalhado

**O que faz**: Extrai perfil detalhado de um instrumento específico com características tímbricas.

**Uso básico**:
```python
iara_revelar_alma_do_instrumento("/Users/vitor/Desktop/musica.mp3", "vocals")
```

**Parâmetros**:
- `file_path`: Arquivo a analisar
- `instrument_type`: Instrumento específico a perfilar

**Quando usar**: Para produção musical, quando precisa entender as características de um instrumento.

---

### 13. `iara_mostrar_sabedoria_classificadora` - Capacidades do Sistema

**O que faz**: Lista instrumentos suportados e métodos de classificação disponíveis.

**Uso básico**:
```python
iara_mostrar_sabedoria_classificadora()
```

---

## 🎨 Ferramentas de Visualização

### 14. `iara_visualizar_ondas_do_tempo` - Waveform Temporal

**O que faz**: Gera gráfico waveform mostrando amplitude ao longo do tempo.

**Uso básico**:
```python
# Salva no desktop (modo local)
iara_visualizar_ondas_do_tempo("/Users/vitor/Desktop/musica.mp3", True, True, None)

# Especifica caminho
iara_visualizar_ondas_do_tempo("/Users/vitor/Desktop/musica.mp3", True, True, "/Users/vitor/Desktop/waveform.png")
```

**Parâmetros**:
- `caminho_arquivo`: Arquivo a visualizar
- `mostrar_envelope`: Mostrar envelope de amplitude
- `normalizar`: Normalizar amplitude
- `caminho_saida`: Onde salvar (None para automático)

**Quando usar**: Para visualizar dinâmica e estrutura temporal da música.

---

### 15. `iara_criar_mapa_das_frequencias` - Espectrogramas

**O que faz**: Gera espectrograma mostrando distribuição de frequências ao longo do tempo.

**Uso básico**:
```python
# Espectrograma STFT padrão
iara_criar_mapa_das_frequencias("/Users/vitor/Desktop/musica.mp3", "stft", None, 512, 2048)

# Espectrograma Mel (perceptual)
iara_criar_mapa_das_frequencias("/Users/vitor/Desktop/musica.mp3", "mel", "/Users/vitor/Desktop/spec.png", 256, 1024)
```

**Parâmetros**:
- `caminho_arquivo`: Arquivo a analisar
- `tipo_espectrograma`: `"stft"`, `"mel"`, `"cqt"`
- `caminho_saida`: Onde salvar
- `tamanho_salto`: Resolução temporal (menor = mais detalhe)
- `tamanho_fft`: Resolução em frequência

**Tipos de espectrogramas**:
- `"stft"`: Geral, boa para análise técnica
- `"mel"`: Perceptual, boa para voz e música
- `"cqt"`: Musical, mostra notas e harmonias

**Quando usar**: Para análise visual de conteúdo espectral e harmônico.

---

### 16. `iara_pintar_essencia_musical` - Visualização de Features

**O que faz**: Gera gráficos de características musicais extraídas (features).

**Uso básico**:
```python
# Visualização completa
iara_pintar_essencia_musical("/Users/vitor/Desktop/musica.mp3", "comprehensive", None)

# Apenas features espectrais
iara_pintar_essencia_musical("/Users/vitor/Desktop/musica.mp3", "spectral", "/Users/vitor/Desktop/features.png")
```

**Tipos de plots**:
- `"comprehensive"`: Todas as características
- `"spectral"`: Features espectrais
- `"rhythmic"`: Características rítmicas

**Quando usar**: Para entender as características musicais extraídas pela análise.

---

### 17. `iara_desenhar_correntes_separadas` - Comparação de Stems

**O que faz**: Cria gráficos comparativos dos stems separados.

**Uso básico**:
```python
iara_desenhar_correntes_separadas("/Users/vitor/Desktop/musica.mp3", "htdemucs_ft", None)
```

**Quando usar**: Para visualizar qualidade da separação de fontes.

---

### 18. `iara_revelar_artes_visuais` - Tipos de Visualizações

**O que faz**: Lista todos os tipos de gráficos e visualizações disponíveis.

**Uso básico**:
```python
iara_revelar_artes_visuais()
```

---

## ⚡ Ferramentas de Otimização

### 19. `iara_mostrar_poder_das_aguas` - Estatísticas de Performance

**O que faz**: Exibe estatísticas detalhadas de performance do sistema.

**Uso básico**:
```python
iara_mostrar_poder_das_aguas()
```

**Exemplo de resultado**:
```json
{
  "cache_stats": {
    "hits": 45,
    "misses": 12,
    "hit_rate": 0.79
  },
  "processing_times": {
    "average_analysis": 8.2,
    "average_separation": 42.1
  },
  "memory_usage": {
    "current_mb": 256,
    "peak_mb": 512
  },
  "system_info": {
    "cpu_count": 8,
    "max_workers": 4
  }
}
```

**Quando usar**: Para monitorar performance e identificar gargalos.

---

### 20. `iara_purificar_memorias` - Limpeza de Cache

**O que faz**: Limpa todo o cache do sistema para liberar memória.

**Uso básico**:
```python
iara_purificar_memorias()
```

**Quando usar**: Quando o sistema está usando muita memória ou você quer garantir resultados atualizados.

---

### 21. `iara_harmonizar_fluxo_musical` - Workflow Otimizado

**O que faz**: Executa múltiplas operações de forma paralela e eficiente.

**Uso básico**:
```python
# Análise + classificação (rápido)
iara_harmonizar_fluxo_musical("/Users/vitor/Desktop/musica.mp3", ["analysis", "classification"], True)

# Workflow completo
iara_harmonizar_fluxo_musical("/Users/vitor/Desktop/musica.mp3", ["analysis", "separation", "classification", "visualization"], True)
```

**Operações disponíveis**:
- `"analysis"`: Análise musical completa
- `"separation"`: Separação de fontes
- `"classification"`: Classificação de instrumentos
- `"visualization"`: Geração de visualizações

**Quando usar**: Para processamento completo eficiente de uma música.

---

### 22. `iara_compartilhar_sabedoria_otimizacao` - Informações de Otimização

**O que faz**: Fornece informações sobre recursos de otimização e recomendações.

**Uso básico**:
```python
iara_compartilhar_sabedoria_otimizacao()
```

---

## 🎯 Workflows Recomendados

### Workflow 1: Análise Básica Rápida
```python
# 1. Despertar e validar
iara_despertar("Começando análise")
iara_validar_cristais_sonoros("musica.mp3")

# 2. Análise básica
iara_mergulhar_nas_ondas("musica.mp3", "basica")

# 3. Visualização simples
iara_visualizar_ondas_do_tempo("musica.mp3", True, True, None)
```

### Workflow 2: Análise Completa Profissional
```python
# 1. Análise completa otimizada
iara_harmonizar_fluxo_musical("musica.mp3", ["analysis", "classification"], True)

# 2. Relatório formatado
iara_tecer_relatorio_das_aguas("musica.mp3", "json", True)

# 3. Visualizações detalhadas
iara_criar_mapa_das_frequencias("musica.mp3", "mel", None, 256, 1024)
iara_pintar_essencia_musical("musica.mp3", "comprehensive", None)
```

### Workflow 3: Separação e Remix
```python
# 1. Comparar modelos de separação
iara_comparar_magias_separadoras("musica.mp3", ["htdemucs_ft", "htdemucs"], ["quality", "speed"])

# 2. Separação com melhor modelo
iara_separar_correntes_musicais("musica.mp3", "demucs", "htdemucs_ft", "wav", None)

# 3. Análise individual dos stems
iara_examinar_corrente_isolada("stems/vocals.wav", "vocals")
iara_examinar_corrente_isolada("stems/drums.wav", "drums")

# 4. Visualização comparativa
iara_desenhar_correntes_separadas("musica.mp3", "htdemucs_ft", None)
```

### Workflow 4: Catalogação de Biblioteca
```python
# 1. Análise em lote
iara_explorar_caverna_sonora("/Users/vitor/Music/", [".mp3", ".m4a", ".wav"])

# 2. Classificação automática (para cada arquivo encontrado)
iara_reconhecer_instrumentos_das_aguas("arquivo.mp3", True, 0.7, "hibrido")

# 3. Relatórios individuais
iara_tecer_relatorio_das_aguas("arquivo.mp3", "json", False)
```

## 🔧 Dicas de Uso

### Performance
- Use `"basica"` para análise rápida em lotes grandes
- Ative `usar_separacao=True` para melhor classificação de instrumentos
- Use `iara_harmonizar_fluxo_musical` para operações paralelas
- Limpe cache com `iara_purificar_memorias` periodicamente

### Qualidade
- Para separação: `htdemucs_ft` oferece melhor qualidade
- Para classificação: `limiar_confianca=0.8` é mais preciso
- Para visualizações: `tipo_espectrograma="mel"` é mais musical

### Compatibilidade
- O sistema detecta automaticamente ambiente local vs. remoto
- Arquivos grandes podem demorar mais (especialmente separação)
- Use formatos sem compressão (WAV, FLAC) para melhor qualidade

---

🧜‍♀️ *"Com estas 22 ferramentas, a Iara revela todos os segredos das águas musicais. Use sua sabedoria ancestral para descobrir as profundezas sonoras de qualquer música."*