# 🧜‍♀️ IaraMCP Dockerfile - Portal das Águas Musicais
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements-docker.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt uvicorn

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
