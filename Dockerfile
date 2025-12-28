FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project metadata
COPY pyproject.toml README.md ./

# Copy backend code
COPY app ./app

# Install project and dependencies
RUN uv pip install --system --no-cache .

# Copy default config and scripts
COPY config.example.json ./config.json
COPY scripts ./scripts

# Create directories for persistent data
RUN mkdir -p logs data && chmod 777 logs data

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)"

# Start FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]