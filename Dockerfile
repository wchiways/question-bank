# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/admin
COPY admin/package.json admin/package-lock.json ./
RUN npm ci
COPY admin/ ./
RUN npm run build

# Stage 2: Build Backend and Final Image
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
# Install uv for faster package management
RUN pip install uv && uv pip install --system -e .

# Copy backend code
COPY app ./app
COPY config.example.json ./config.json
COPY scripts ./scripts

# Copy built frontend assets
COPY --from=frontend-builder /app/admin/dist ./app/static/admin

# Create directory for logs and db
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
