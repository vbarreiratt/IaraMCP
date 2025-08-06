# 🧜‍♀️ IaraMCP Dockerfile LITE - Versão Leve para Smithery
FROM python:3.11-slim

# Instalar apenas dependências essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependências Python LEVES (sem PyTorch/Demucs)
COPY requirements-lite.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY ./src ./src
COPY pyproject.toml ./

# Configurar variáveis de ambiente
ENV PYTHONPATH=/app \
    IARAMCP_VIS_MODE=web

# Usar variável PORT do ambiente
EXPOSE ${PORT:-3333}

# Health check leve
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:${PORT:-3333}/ || exit 1

# Comando que usa PORT do ambiente
CMD uvicorn src.iaramcp.server_fastmcp:app --host 0.0.0.0 --port ${PORT:-3333}