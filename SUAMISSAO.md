# 🧜‍♀️ IaraMCP - Prompt de Refatoração e Preparação para Smithery.ai

## 📋 CONTEXTO ATUAL

O projeto IaraMCP é um servidor MCP (Model Context Protocol) robusto para análise musical avançada com temática da mitologia brasileira da Iara. Após extensas edições e testes locais com o inspetor MCP, o projeto está funcional mas precisa de:

1. **Validação de compatibilidade** com Claude Desktop
2. **Limpeza de arquivos desnecessários**
3. **Preparação para deployment** no Smithery.ai
4. **Documentação profissional** organizada

---

## 🎯 OBJETIVOS PRINCIPAIS

### 1️⃣ **VALIDAÇÃO DE FUNCIONALIDADE CROSS-PLATFORM**

**OBJETIVO**: Garantir que todas as ferramentas funcionem tanto localmente (MCP Inspector) quanto remotamente (Claude Desktop).

**TAREFAS ESPECÍFICAS**:
- [ ] **Revisar sistema de fallback de output_path**: Verificar se o mecanismo automático funciona corretamente
  - Local: Salva arquivos no diretório especificado
  - Remoto: Retorna base64 ou dados que o Claude possa processar
- [ ] **Testar todas as 20+ ferramentas** individualmente:
  - `iara_mergulhar_nas_ondas()` - Análise completa
  - `iara_separar_correntes_musicais()` - Separação com Demucs
  - `iara_reconhecer_instrumentos_das_aguas()` - Detecção de instrumentos
  - `iara_visualizar_ondas_do_tempo()` - Visualizações
  - Todas as outras ferramentas conforme documentação
- [ ] **Verificar paths e dependências**: Garantir que paths absolutos não quebrem em diferentes ambientes
- [ ] **Validar outputs**: Confirmar que imagens/arquivos são acessíveis tanto local quanto remotamente

### 2️⃣ **LIMPEZA E ORGANIZAÇÃO DO PROJETO**

**OBJETIVO**: Manter apenas arquivos essenciais e criar documentação profissional.

**ARQUIVOS PARA MANTER**:
```
IaraMCP/
├── src/iaramcp/           # Código fonte principal
├── README.md              # Documentação principal (tema Iara)
├── AGENTE.md              # Manual técnico para agentes/desenvolvedores
├── MANUAL.md              # Manual completo de uso
├── pyproject.toml         # Configuração do projeto
├── smithery.yaml          # Configuração Smithery.ai
├── Dockerfile             # Container para Smithery.ai
├── requirements.txt       # Dependências Python
├── .gitignore            # Arquivos ignorados
└── LICENSE               # Licença do projeto
```

**ARQUIVOS PARA REMOVER**:
- Todos os arquivos temporários criados durante desenvolvimento
- Documentos duplicados ou redundantes
- Arquivos de teste não essenciais
- Qualquer arquivo que não seja crítico para funcionamento

**DOCUMENTOS A CRIAR/REESCREVER**:

1. **README.md** - Versão final com:
   - Apresentação temática da Iara
   - Instalação e configuração
   - Exemplos de uso básico
   - Badges e links relevantes

2. **AGENTE.md** - Manual técnico contendo:
   - Arquitetura completa do sistema
   - Descrição detalhada de cada módulo
   - APIs e interfaces internas
   - Guia de contribuição e desenvolvimento
   - Debugging e troubleshooting
   - Comandos shell necessarios para iniciar ambiente de desenvolvimento/ trabalho

3. **MANUAL.md** - Manual completo com:
   - Todas as 20+ ferramentas disponíveis
   - Exemplos práticos de cada ferramenta
   - Workflows recomendados
   - Casos de uso avançados

### 3️⃣ **ANÁLISE E PREPARAÇÃO PARA SMITHERY.AI**

**OBJETIVO**: Entender requisitos do Smithery.ai e preparar projeto adequadamente.

**TAREFAS DE ANÁLISE**:
- [ ] **Pesquisar especificações do Smithery.ai**:
  - Estrutura de projeto esperada
  - Configurações obrigatórias no `smithery.yaml`
  - Requisitos do `Dockerfile`
  - Limitações de ambiente e dependências
  
- [ ] **Analisar arquivos atuais**:
  - Validar `smithery.yaml` atual
  - Revisar `Dockerfile` para compliance
  - Verificar se `pyproject.toml` está correto
  
- [ ] **Teste local do container**:
  - Debuggar problemas do Docker local
  - Garantir que todas dependências sejam instaladas
  - Testar funcionamento completo em container

**DECISÃO ESTRATÉGICA**:
- [ ] **Avaliar necessidade de branch separado**:
  - Se adaptações forem mínimas: manter projeto único
  - Se adaptações forem significativas: criar branch `smithery-deployment`
  - Documentar diferenças entre versões

### 4️⃣ **PREPARAÇÃO FINAL PARA SMITHERY.AI**

**OBJETIVO**: Deixar projeto pronto para deployment imediato.

**CONFIGURAÇÕES OBRIGATÓRIAS**:
- [ ] **smithery.yaml otimizado**:
  - Metadata correto do projeto
  - Configurações de ambiente
  - Dependências e recursos necessários

- [ ] **Dockerfile funcional**:
  - Base image adequada
  - Instalação correta de dependências (ffmpeg, librosa, demucs, etc.)
  - Exposição de portas corretas
  - Comando de inicialização apropriado

- [ ] **Testes finais**:
  - Build do Docker sem erros
  - Execução completa do container
  - Teste de conectividade MCP
  - Validação de todas as ferramentas

---

## 🔧 ESPECIFICAÇÕES TÉCNICAS

### **DEPENDÊNCIAS CRÍTICAS**:
```python
# Audio processing
librosa>=0.10.0
demucs>=4.0.0
torch>=2.0.0
torchaudio>=2.0.0
soundfile>=0.12.0

# MCP Framework
fastmcp
asyncio

# ML & Analysis
scikit-learn>=1.0.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0

# System dependencies (Docker)
ffmpeg
```

### **ESTRUTURA DE FALLBACK**:
```python
def _determine_output_path(self, base_path: str = None) -> Optional[str]:
    """Determina path de output com fallback automático"""
    if self.is_local_environment():
        return base_path or "/tmp/iaramcp_output"
    else:
        return None  # Força retorno base64 para ambientes remotos
```

### **CONFIGURAÇÃO MCP**:
```json
{
  "mcpServers": {
    "iaramcp": {
      "command": "python",
      "args": ["-m", "iaramcp.server_fastmcp"],
      "env": {
        "PYTHONPATH": "/path/to/iaramcp/src"
      }
    }
  }
}
```

---

## 📝 CRITÉRIOS DE SUCESSO

### ✅ **FUNCIONALIDADE**:
- [ ] Todas as 20+ ferramentas funcionam local e remotamente
- [ ] Sistema de fallback opera corretamente
- [ ] Outputs são acessíveis em ambos ambientes
- [ ] Performance mantida após refatoração

### ✅ **ORGANIZAÇÃO**:
- [ ] Projeto limpo com apenas arquivos essenciais
- [ ] Documentação profissional e completa
- [ ] Estrutura clara e navegável
- [ ] Código bem documentado e comentado

### ✅ **DEPLOYMENT**:
- [ ] Docker build e run sem erros
- [ ] Smithery.ai configurations válidas
- [ ] Testes de integração passando
- [ ] Pronto para upload no Smithery.ai

### ✅ **QUALIDADE**:
- [ ] Código segue padrões Python
- [ ] Tratamento de erros robusto
- [ ] Logs informativos implementados
- [ ] Performance otimizada

---

## 🚀 ENTREGÁVEIS FINAIS

1. **Projeto IaraMCP refatorado** com estrutura limpa
2. **Documentação completa** (README, AGENTE, MANUAL)
3. **Configuração Smithery.ai validada** (smithery.yaml, Dockerfile)
4. **Relatório de compatibilidade** local vs remoto
5. **Instruções de deployment** para Smithery.ai

---

## ⚠️ CONSIDERAÇÕES IMPORTANTES

- **Manter temática da Iara** em toda documentação
- **Preservar funcionalidades existentes** durante refatoração
- **Priorizar compatibilidade** sobre funcionalidades experimentais
- **Documentar todas as mudanças** realizadas
- **Testar exhaustivamente** antes de finalizar

---

## 📞 PRÓXIMOS PASSOS

1. **EXECUTAR** este prompt com Claude Code
2. **REVISAR** cada entregável produzido
3. **TESTAR** funcionalidades em ambos ambientes
4. **AJUSTAR** configurações conforme necessário
5. **DEPLOY** no Smithery.ai

---

*"Que a sabedoria da Iara guie este processo de refatoração, transformando complexidade em simplicidade e caos em harmonia, como as águas que fluem naturalmente em direção ao mar."* 🧜‍♀️🌊