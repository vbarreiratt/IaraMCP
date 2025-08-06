# 🧜‍♀️ IaraMCP Dockerfile - Portal das Águas Musicais
# Multi-stage build otimizado para resolver problemas de timeout

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Instalar dependências do sistema necessárias para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    ffmpeg \
    git \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Criar virtual environment
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copiar arquivos de dependências primeiro (otimização de cache)
COPY arquivo/requirements-docker.txt requirements.txt
COPY pyproject.toml ./

# Instalar dependências com cache mount para otimizar builds subsequentes
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt uvicorn

# Stage 2: Runtime image
FROM python:3.11-slim

# Instalar apenas dependências de runtime necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar virtual environment do stage de build
COPY --from=builder /app/venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copiar código fonte
COPY ./src ./src
COPY pyproject.toml README.md ./

# Configurar variáveis de ambiente
ENV PYTHONPATH=/app \
    IARAMCP_VIS_MODE=web \
    PORT=3333

# Expor porta
EXPOSE 3333

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:3333/ || exit 1

# Comando de inicialização
CMD ["uvicorn", "src.iaramcp.server_fastmcp:app", "--host", "0.0.0.0", "--port", "3333", "--workers", "1"]
