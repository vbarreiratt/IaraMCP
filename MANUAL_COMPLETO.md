# 🧜‍♀️ IaraMCP - Manual Completo para Iniciantes

*Guia extremamente detalhado para usar o IaraMCP - Servidor de Análise Musical da Iara*

## 📋 Índice Rápido
1. [O que é o IaraMCP](#o-que-é-o-iaramcp)
2. [Requisitos do Sistema](#requisitos-do-sistema)
3. [Verificação de Dependências](#verificação-de-dependências)
4. [Como Iniciar o Servidor (3 métodos)](#como-iniciar-o-servidor)
5. [Usando com Claude Desktop](#usando-com-claude-desktop)
6. [Usando com MCP Inspector](#usando-com-mcp-inspector)
7. [Testando o Funcionamento](#testando-o-funcionamento)
8. [Solução de Problemas](#solução-de-problemas)

---

## 🌊 O que é o IaraMCP?

IaraMCP é um servidor que permite ao Claude Desktop analisar arquivos de música. Ele se chama "Iara" em homenagem à sereia da mitologia brasileira que tinha poderes musicais. O servidor pode:

- ✅ Analisar características musicais (tempo, tom, ritmo)
- ✅ Separar instrumentos em faixas diferentes 
- ✅ Identificar que tipos de instrumentos estão tocando
- ✅ Criar gráficos visuais da música
- ✅ Processar arquivos MP3, WAV, FLAC, M4A, OGG

---

## 💻 Requisitos do Sistema

**Seu computador precisa ter:**
- macOS (que você já tem)
- Python 3.8 ou superior (já instalado via Anaconda)
- Node.js e npm (já instalados)
- Pelo menos 4GB de RAM livre
- Espaço em disco: 2GB livres

**Localização dos arquivos:**
- Projeto IaraMCP: `/Users/vitor/Desktop/IaraMCP/`
- Python do Anaconda: `/opt/anaconda3/bin/python`

---

## 🔍 Verificação de Dependências

Antes de começar, vamos verificar se tudo está instalado corretamente.

### Passo 1: Abrir o Terminal
1. Pressione `Cmd + Espaço` (Spotlight)
2. Digite "Terminal"
3. Pressione Enter

### Passo 2: Verificar Python
Digite no terminal e pressione Enter:
```bash
/opt/anaconda3/bin/python --version
```
**Resultado esperado:** `Python 3.12.x` (ou versão similar)

### Passo 3: Verificar dependências do IaraMCP
Digite no terminal:
```bash
PYTHONPATH=/Users/vitor/Desktop/IaraMCP/src /opt/anaconda3/bin/python -c "
try:
    import iaramcp.server_fastmcp
    print('✅ IaraMCP está funcionando!')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```
**Resultado esperado:** `✅ IaraMCP está funcionando!`

### Passo 4: Verificar MCP Inspector
Digite no terminal:
```bash
mcp-inspector --help
```
**Resultado esperado:** Uma lista de opções de uso

---

## 🚀 Como Iniciar o Servidor

Existem **3 maneiras** de usar o IaraMCP:

### 🌟 MÉTODO 1: Usar com Claude Desktop (Recomendado para uso normal)

**Quando usar:** Para conversar com Claude e pedir análises musicais de forma natural.

**Como funciona:** O Claude Desktop conecta automaticamente ao servidor.

**Passos:**

#### 1.1 Verificar se a configuração está correta
Abra o arquivo de configuração:
```bash
open "/Users/vitor/Library/Application Support/Claude/claude_desktop_config.json"
```

Verifique se tem exatamente isto:
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

#### 1.2 Fechar completamente o Claude Desktop
- Clique em "Claude" no menu superior
- Clique em "Quit Claude" (ou pressione Cmd+Q)
- **IMPORTANTE:** Espere 5 segundos

#### 1.3 Abrir novamente o Claude Desktop
- Abra o Claude Desktop normalmente
- Procure por um ícone pequeno ou indicação de "MCP" na interface
- Se ver "iaramcp" conectado, está funcionando!

#### 1.4 Testar no Claude
Digite no chat:
```
Use iara_despertar para verificar se a Iara está funcionando
```

---

### 🔍 MÉTODO 2: Usar com MCP Inspector (Para desenvolvedores/testes)

**Quando usar:** Para testar ferramentas individualmente, ver detalhes técnicos, ou resolver problemas.

**Como funciona:** Interface web que mostra todas as ferramentas disponíveis.

**Passos:**

#### 2.1 Abrir DOIS terminais
- Terminal 1: Para o servidor IaraMCP
- Terminal 2: Para o MCP Inspector

**Como abrir dois terminais:**
1. Abra o Terminal (Cmd+Espaço → "Terminal")
2. Pressione Cmd+T para abrir uma nova aba
3. Ou pressione Cmd+N para nova janela

#### 2.2 No Terminal 1 (Servidor IaraMCP)
Digite exatamente:
```bash
cd /Users/vitor/Desktop/IaraMCP
PYTHONPATH=./src /opt/anaconda3/bin/python -m iaramcp.server_fastmcp
```

**O que você verá:**
```
Starting MCP server...
Server streams initialized
```
**IMPORTANTE:** Deixe este terminal aberto e funcionando!

#### 2.3 No Terminal 2 (MCP Inspector)
Digite exatamente:
```bash
cd /Users/vitor/Desktop/IaraMCP
./start_inspector_correto.sh
```

**O que você verá:**
```
Starting MCP inspector...
Server URL: http://localhost:5173
```

#### 2.4 Abrir no navegador
1. Abra seu navegador (Safari, Chrome, etc.)
2. Vá para: `http://localhost:5173`
3. Você verá uma interface com todas as ferramentas da Iara!

#### 2.5 Como parar
- Para parar o Inspector: Pressione Ctrl+C no Terminal 2
- Para parar o Servidor: Pressione Ctrl+C no Terminal 1

---

### ⚡ MÉTODO 3: Teste Rápido (Para verificar se funciona)

**Quando usar:** Para verificar rapidamente se tudo está funcionando.

**Passos:**

#### 3.1 Abrir Terminal
```bash
cd /Users/vitor/Desktop/IaraMCP
python test_basic.py
```

**Resultado esperado:**
```
🎵 Testing IaraMCP Analysis Server
==================================================
✅ File valid: True
✅ Basic analysis completed!
✅ All tests passed!
```

---

## 💬 Usando com Claude Desktop

### Comandos que você pode usar no Claude:

#### Comandos Básicos da Iara:
```
Use iara_despertar para verificar se está funcionando

Use iara_validar_cristais_sonoros com o arquivo "/caminho/para/musica.mp3"

Use iara_mergulhar_nas_ondas para analisar "/caminho/para/musica.mp3"
```

#### Análise Completa:
```
Iara, mergulhe nas águas do arquivo "/Users/vitor/Desktop/musica.mp3" e me conte todos os segredos musicais que encontrar
```

#### Separação de Instrumentos:
```
Use iara_separar_correntes_musicais para separar o arquivo "/Users/vitor/Desktop/musica.mp3" em instrumentos individuais
```

#### Visualizações:
```
Use iara_visualizar_ondas_do_tempo para criar um gráfico do arquivo "/Users/vitor/Desktop/musica.mp3"

Use iara_criar_mapa_das_frequencias para mostrar as frequências da música
```

### 📁 Como encontrar o caminho correto dos arquivos:

1. **Método fácil:** Arraste o arquivo para o Terminal
   - Abra o Terminal
   - Digite: `echo "`
   - Arraste seu arquivo de música para o Terminal
   - Digite: `"`
   - Pressione Enter
   - Copie o caminho que apareceu

2. **Exemplo de caminhos típicos:**
   - Desktop: `/Users/vitor/Desktop/NomeDaMusica.mp3`
   - Downloads: `/Users/vitor/Downloads/NomeDaMusica.mp3`
   - Música: `/Users/vitor/Music/NomeDaMusica.mp3`

---

## 🔍 Usando com MCP Inspector

### Interface Web do Inspector:

Quando você abrir `http://localhost:5173`, verá:

#### Seção "Tools" (Ferramentas):
- Lista de todas as ferramentas da Iara
- Clique em qualquer ferramenta para ver detalhes
- Cada ferramenta mostra:
  - Nome temático (ex: `iara_despertar`)
  - Descrição do que faz
  - Parâmetros necessários

#### Como testar uma ferramenta:
1. Clique na ferramenta desejada
2. Preencha os parâmetros (ex: caminho do arquivo)
3. Clique em "Call Tool"
4. Veja o resultado na parte inferior

#### Ferramentas mais úteis para testar:
1. **`iara_despertar`** - Não precisa de parâmetros
2. **`iara_validar_cristais_sonoros`** - Precisa do caminho do arquivo
3. **`iara_mergulhar_nas_ondas`** - Análise completa (demora mais)

---

## 🧪 Testando o Funcionamento

### Teste 1: Verificar se o servidor inicia
```bash
cd /Users/vitor/Desktop/IaraMCP
PYTHONPATH=./src /opt/anaconda3/bin/python -c "
try:
    import iaramcp.server_fastmcp
    print('✅ Servidor OK')
except Exception as e:
    print(f'❌ Erro: {e}')
"
```

### Teste 2: Testar com arquivo real
1. Coloque um arquivo MP3 no Desktop
2. No Claude Desktop, digite:
```
Use iara_despertar
```
3. Depois:
```
Use iara_validar_cristais_sonoros com "/Users/vitor/Desktop/NOME_DO_SEU_ARQUIVO.mp3"
```

### Teste 3: Análise completa
```
Use iara_mergulhar_nas_ondas para analisar "/Users/vitor/Desktop/NOME_DO_SEU_ARQUIVO.mp3" com tipo_analise "completa"
```

---

## 🔧 Solução de Problemas

### ❌ Problema: "Module not found" ou erro de importação

**Solução:**
```bash
cd /Users/vitor/Desktop/IaraMCP
/opt/anaconda3/bin/pip install -r requirements.txt
```

### ❌ Problema: Claude Desktop não vê o servidor

**Soluções:**
1. Verifique o arquivo de configuração:
```bash
cat "/Users/vitor/Library/Application Support/Claude/claude_desktop_config.json"
```

2. Feche COMPLETAMENTE o Claude Desktop (Cmd+Q)
3. Espere 10 segundos
4. Abra novamente

### ❌ Problema: "File not found" ao analisar música

**Soluções:**
1. Verifique se o arquivo existe:
```bash
ls -la "/caminho/para/seu/arquivo.mp3"
```

2. Use o método de arrastar arquivo para ter certeza do caminho correto

### ❌ Problema: MCP Inspector não abre

**Soluções:**
1. **Verificar se a porta está livre:**
```bash
lsof -i :5173
```

2. **Matar processos na porta se necessário:**
```bash
killall -9 node
```

3. **Executar manualmente:**
```bash
cd /Users/vitor/Desktop/IaraMCP
mcp-inspector --config inspector_config.json --server iaramcp
```

### ❌ Problema: Servidor trava ou fica lento

**Soluções:**
1. Feche e reabra os terminais
2. Reinicie o computador se necessário
3. Verifique espaço em disco:
```bash
df -h
```

### ❌ Problema: Erro "Permission denied"

**Soluções:**
```bash
chmod +x /Users/vitor/Desktop/IaraMCP/src/iaramcp/*.py
```

---

## 📚 Resumo dos Comandos Mais Importantes

### Para usar com Claude Desktop:
1. Configurar arquivo: `/Users/vitor/Library/Application Support/Claude/claude_desktop_config.json`
2. Fechar e abrir Claude Desktop
3. Testar: `Use iara_despertar`

### Para usar com MCP Inspector:
```bash
# Terminal 1:
cd /Users/vitor/Desktop/IaraMCP
./start_iaramcp.sh

# Terminal 2:
cd /Users/vitor/Desktop/IaraMCP
./start_inspector_correto.sh

# Navegador: http://localhost:5173
```

### Para teste básico:
```bash
cd /Users/vitor/Desktop/IaraMCP
python test_basic.py
```

### Para verificar se tudo funciona:
```bash
PYTHONPATH=/Users/vitor/Desktop/IaraMCP/src /opt/anaconda3/bin/python -c "import iaramcp.server_fastmcp; print('✅ OK')"
```

---

## 🎵 Lista Completa das Ferramentas da Iara

### Essenciais:
- `iara_despertar` - Verifica se está funcionando
- `iara_validar_cristais_sonoros` - Valida arquivo de música
- `iara_mergulhar_nas_ondas` - Análise musical completa

### Separação:
- `iara_separar_correntes_musicais` - Separa instrumentos
- `iara_examinar_corrente_isolada` - Analisa instrumento separado
- `iara_comparar_magias_separadoras` - Compara métodos

### Visualização:
- `iara_visualizar_ondas_do_tempo` - Gráfico da música
- `iara_criar_mapa_das_frequencias` - Mapa de frequências
- `iara_pintar_essencia_musical` - Gráficos de características

### Avançadas:
- `iara_reconhecer_instrumentos_das_aguas` - Identifica instrumentos
- `iara_tecer_relatorio_das_aguas` - Relatório completo
- `iara_explorar_caverna_sonora` - Analisa pasta inteira
- `iara_harmonizar_fluxo_musical` - Processamento otimizado

---

🧜‍♀️ **Lembre-se:** A Iara é uma sereia brasileira, então trate-a com carinho! Se algo não funcionar, consulte este manual ou tente reiniciar tudo. Boa sorte com suas análises musicais!