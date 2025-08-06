# 🧜‍♀️ IaraMCP - Guia Multi-Transporte

*Como usar o IaraMCP com Claude Desktop E MCP Inspector*

## 🌊 O Problema Resolvido

Antes: O servidor só funcionava com Claude Desktop OU com MCP Inspector, mas não com ambos.

Agora: A Iara pode operar em diferentes modos para máxima compatibilidade!

---

## 🚀 Modos Disponíveis

### 📝 **Modo STDIO (Claude Desktop)**
- **Para:** Conversas naturais com Claude
- **Compatível:** Claude Desktop
- **Não compatível:** MCP Inspector

### 🌐 **Modo HTTP (MCP Inspector)**
- **Para:** Interface web de testes e desenvolvimento
- **Compatível:** MCP Inspector, ferramentas web
- **Não compatível:** Claude Desktop

### 📡 **Modo SSE (Ferramentas Avançadas)**
- **Para:** Integração com Langflow e outras ferramentas
- **Compatível:** Server-Sent Events, WebSockets
- **Não compatível:** Claude Desktop

---

## 🎯 Cenários de Uso

### **Cenário 1: Apenas Claude Desktop**
```bash
cd /Users/vitor/Desktop/IaraMCP
./start_iaramcp.sh
```
- Configure Claude Desktop com `claude_desktop_config_exemplo.json`
- Reinicie Claude Desktop
- Digite: `Use iara_despertar`

### **Cenário 2: Apenas MCP Inspector**
```bash
# Terminal 1:
cd /Users/vitor/Desktop/IaraMCP
./start_iaramcp_http.sh

# Terminal 2:
cd /Users/vitor/Desktop/IaraMCP
./start_inspector_http.sh

# Navegador: http://localhost:5173
```

### **Cenário 3: Alternar entre modos**
```bash
cd /Users/vitor/Desktop/IaraMCP
./start_iaramcp_escolher.sh
```
Escolha o modo interativamente.

### **Cenário 4: Desenvolvimento/Debug**
Use ambos alternadamente:
1. Teste no Inspector para ver detalhes técnicos
2. Pare o servidor HTTP (Ctrl+C)
3. Inicie em modo STDIO para usar com Claude Desktop
4. Teste a conversa natural

---

## 📋 Scripts Disponíveis

### **Básicos:**
- `start_iaramcp.sh` - Modo STDIO (Claude Desktop)
- `start_iaramcp_http.sh` - Modo HTTP (Inspector)
- `start_inspector_http.sh` - Inspector conecta via HTTP

### **Avançados:**
- `start_iaramcp_escolher.sh` - Menu interativo
- `start_inspector_correto.sh` - Inspector modo antigo (não recomendado)

### **Configuração:**
- `claude_desktop_config_exemplo.json` - Configure Claude Desktop

---

## ⚡ Início Rápido

### **Para usar com Claude Desktop AGORA:**
1. `./start_iaramcp.sh` 
2. Configure Claude Desktop
3. Reinicie Claude Desktop
4. Teste: `Use iara_despertar`

### **Para usar com Inspector AGORA:**
1. Terminal 1: `./start_iaramcp_http.sh`
2. Terminal 2: `./start_inspector_http.sh` 
3. Navegador: `http://localhost:5173`

---

## 🔧 Resolução de Problemas

### **❌ Inspector não conecta**
- Certifique-se de usar `start_iaramcp_http.sh` (modo HTTP)
- Verifique se http://localhost:3333 está respondendo
- Use `./start_inspector_http.sh` (não o antigo)

### **❌ Claude Desktop não vê servidor**
- Use `start_iaramcp.sh` (modo STDIO) 
- Atualize configuração com `claude_desktop_config_exemplo.json`
- Reinicie Claude Desktop completamente

### **❌ Porta ocupada**
```bash
lsof -i :3333  # Verificar porta HTTP
lsof -i :5173  # Verificar porta Inspector
killall node   # Matar processos se necessário
```

---

## 🌟 Vantagens da Solução

✅ **Compatibilidade Total:** Funciona com Claude Desktop E Inspector  
✅ **Flexibilidade:** Escolha o modo conforme a necessidade  
✅ **Sem Conflitos:** Modos separados evitam problemas de comunicação  
✅ **Fácil de Usar:** Scripts automatizados para cada cenário  
✅ **Futuro-Proof:** Suporte a SSE para ferramentas avançadas  

---

🧜‍♀️ **A Iara agora flui em todas as águas digitais!**