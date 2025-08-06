# Prompt para Claude Code: Debug de Erro Smithery MCP Deploy

Analise meu projeto para identificar possíveis causas do erro `"Using Dockerfile from repository Unexpected internal error or timeout"` no deploy do Smithery. Verifique sistematicamente cada item abaixo:

## 📋 Checklist de Verificação

### 1. **Estrutura e Localização de Arquivos**
- [ ] Verificar se existe `Dockerfile` na raiz do projeto ou no caminho especificado
- [ ] Verificar se existe `smithery.yaml` na raiz do projeto
- [ ] Confirmar se os caminhos em `smithery.yaml` estão corretos

### 2. **Configuração do smithery.yaml**
- [ ] Verificar se `runtime: "container"` está definido
- [ ] Validar configuração da seção `build`:
  ```yaml
  build:
    dockerfile: "Dockerfile"
    dockerBuildPath: "."
  ```
- [ ] Verificar se `startCommand.type: "http"` está configurado
- [ ] Validar se existe `configSchema` válido

### 3. **Análise do Dockerfile**
- [ ] Verificar se usa distribuição Linux suportada (Alpine, Debian-based)
- [ ] Confirmar se `CMD` ou `ENTRYPOINT` está correto para iniciar servidor HTTP
- [ ] Verificar se `WORKDIR` está definido adequadamente
- [ ] Analisar se comandos `RUN` podem causar timeout (downloads grandes, builds complexos)
- [ ] Verificar se `COPY` inclui todos os arquivos necessários

### 4. **Requisitos de Servidor HTTP**
- [ ] Confirmar se servidor implementa endpoint `/mcp`
- [ ] Verificar se suporta métodos `GET`, `POST`, `DELETE`
- [ ] Validar se servidor escuta na variável de ambiente `PORT`
- [ ] Verificar implementação do protocolo Streamable HTTP

### 5. **Dependências e Build**
- [ ] Analisar `package.json`/`requirements.txt` para dependências problemáticas
- [ ] Verificar se existe `smithery.config.js` com dependências externas configuradas
- [ ] Identificar dependências que podem causar timeout: `playwright-core`, `sharp`, `@grpc/grpc-js`
- [ ] Verificar tamanho das dependências e tempo de instalação

### 6. **Otimizações de Performance**
- [ ] Verificar se usa imagem base apropriada (ex: `node:18-alpine`, `python:3.11-slim`)
- [ ] Analisar se build é eficiente (cache de layers, ordem de COPY)
- [ ] Verificar se há comandos desnecessários que podem causar timeout

### 7. **Configuração de Ambiente e Variáveis**
- [ ] Confirmar se servidor aceita variável `PORT` do ambiente
- [ ] Verificar se variáveis de ambiente necessárias estão definidas
- [ ] Validar configuração de `env` no `smithery.yaml`

## 🔍 Ações Específicas

1. **Examine todos os arquivos relevantes** (Dockerfile, smithery.yaml, package.json, etc.)
2. **Identifique problemas específicos** em cada categoria
3. **Sugira correções detalhadas** para cada problema encontrado
4. **Priorize as correções** por probabilidade de serem a causa do erro
5. **Forneça exemplos de código** correto quando necessário

## 🎯 Resultado Esperado

Forneça um relatório detalhado com:
- ✅ Itens que estão corretos
- ❌ Problemas identificados com explicação
- 🔧 Correções específicas recomendadas
- 📝 Exemplos de código corrigido
- 🚀 Próximos passos para resolver o erro

**Foque especialmente em problemas que podem causar timeout durante o build do Docker ou falhas na inicialização do servidor HTTP.**