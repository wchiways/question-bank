# Docker 部署指南

本文档详细介绍了如何使用 Docker 和 Docker Compose 快速部署并运行 OCS 题库系统，涵盖从基础安装到生产环境部署的完整流程。

## 目录

- [为什么使用 Docker](#为什么使用-docker)
- [环境准备](#环境准备)
- [快速开始](#快速开始)
- [配置详解](#配置详解)
- [部署方式](#部署方式)
  - [方式一：Docker Compose（推荐）](#方式一docker-compose推荐)
  - [方式二：Docker CLI](#方式二docker-cli)
  - [方式三：多容器部署（含 Redis）](#方式三多容器部署含-redis)
- [管理与监控](#管理与监控)
- [常见问题排查](#常见问题排查)
- [生产环境优化](#生产环境优化)
- [安全最佳实践](#安全最佳实践)
- [备份与恢复](#备份与恢复)

---

## 为什么使用 Docker

使用 Docker 部署 OCS 题库系统具有以下优势：

- **环境隔离**: 避免依赖冲突，保证运行环境一致性
- **快速部署**: 一条命令启动整个应用
- **易于扩展**: 支持水平扩展和负载均衡
- **版本管理**: 便于版本回滚和升级
- **资源限制**: 精确控制 CPU、内存使用
- **跨平台**: 支持 Linux、macOS、Windows

---

## 环境准备

### 1. 安装 Docker

#### Linux (Ubuntu/Debian)

```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加 Docker 官方 GPG 密钥
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 设置仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 验证安装
sudo docker run hello-world
```

#### macOS

下载并安装 [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)

#### Windows

下载并安装 [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)

### 2. 配置 Docker 用户组（可选）

避免每次使用 sudo：

```bash
# 创建 docker 组（如果不存在）
sudo groupadd docker

# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 刷新用户组
newgrp docker

# 验证（不需要 sudo）
docker run hello-world
```

### 3. 验证安装

```bash
# 检查 Docker 版本
docker --version
# 输出: Docker version 24.x.x

# 检查 Docker Compose 版本
docker compose version
# 输出: Docker Compose version v2.x.x

# 检查 Docker 状态
sudo systemctl status docker  # Linux
# 或打开 Docker Desktop      # macOS/Windows
```

---

## 快速开始

### 步骤 A：获取项目代码

```bash
# 克隆仓库
git clone https://github.com/wchiways/question-bank.git
cd ocs-tiku

# 或者从已有项目目录进入
cd /path/to/ocs-tiku
```

### 步骤 B：创建持久化目录

```bash
# 创建数据和日志目录
mkdir -p data logs

# 设置权限（Linux/macOS）
chmod 777 data logs

# Windows 用户可以跳过 chmod 命令
```

**目录说明**:
- `data/`: 存储 SQLite 数据库文件
- `logs/`: 存储应用日志

### 步骤 C：配置参数

#### 1. 创建配置文件

```bash
# 复制配置模板
cp config.example.json config.json
```

#### 2. 编辑配置文件

**重要**: 编辑 `config.json`，修改以下关键配置：

##### 数据库配置（必须）

```json
{
  "database": {
    "url": "sqlite+aiosqlite:////app/data/question_bank.db",
    "echo": false
  }
}
```

**路径说明**:
- 容器内路径固定为 `/app/data/question_bank.db`
- 四个斜杠 `////` 表示容器内的绝对路径
- 通过 volume 映射到宿主机的 `./data` 目录

##### AI 服务配置（必须）

```json
{
  "ai": {
    "default_provider": "siliconflow",
    "timeout": 30,
    "max_retries": 3,
    "providers": {
      "siliconflow": {
        "enabled": true,
        "api_key": "YOUR_SILICONFLOW_API_KEY",
        "api_url": "https://api.siliconflow.cn/v1/chat/completions",
        "model": "Qwen/QwQ-32B",
        "max_tokens": 512,
        "temperature": 0.1
      }
    }
  }
}
```

**注意**:
- 将 `YOUR_SILICONFLOW_API_KEY` 替换为你的真实 API Key
- 可以同时配置多个 AI 提供商作为备用

##### 日志配置

```json
{
  "logging": {
    "level": "INFO",
    "file": "/app/logs/app.log",
    "rotation": "10 MB"
  }
}
```

##### 服务器配置

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8000
  }
}
```

### 步骤 D：启动服务

```bash
# 构建并启动容器
docker compose up -d --build

# 查看启动日志
docker compose logs -f

# 等待看到 "Application startup complete" 后按 Ctrl+C 退出日志查看
```

### 步骤 E：验证部署

```bash
# 1. 检查容器状态
docker compose ps

# 应该看到：
# NAME                COMMAND                  SERVICE      STATUS
# ocs-tiku            "uvicorn app.main:ap…"   ocs-tiku     Up (healthy)

# 2. 健康检查
curl http://localhost:8000/health

# 应该返回: {"status":"healthy"}

# 3. 测试查询接口
curl "http://localhost:8000/api/v1/query?title=中国的首都是哪里？&options=A.北京 B.上海"
```

---

## 配置详解

### docker-compose.yml 详解

```yaml
version: '3.8'

services:
  ocs-tiku:
    build: .                    # 使用当前目录的 Dockerfile 构建
    image: ocs-tiku:latest      # 镜像名称和标签
    container_name: ocs-tiku    # 容器名称
    ports:
      - "8000:8000"             # 端口映射: 宿主机:容器
    volumes:
      - ./config.json:/app/config.json:ro        # 配置文件（只读）
      - ./data:/app/data                         # 数据目录
      - ./logs:/app/logs                         # 日志目录
    restart: unless-stopped     # 重启策略
    environment:
      - TZ=Asia/Shanghai        # 时区设置
    healthcheck:                # 健康检查
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s             # 每 30 秒检查一次
      timeout: 10s              # 超时时间
      retries: 3                # 失败重试次数
      start_period: 10s         # 启动等待时间
```

### Dockerfile 详解

```dockerfile
# 基础镜像
FROM python:3.11-slim

# 工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv（包管理器）
RUN pip install --no-cache-dir uv

# 复制项目元数据
COPY pyproject.toml README.md ./

# 复制应用代码
COPY app ./app

# 安装 Python 依赖
RUN uv pip install --system --no-cache .

# 复制配置文件和脚本
COPY config.example.json ./config.json
COPY scripts ./scripts

# 创建持久化目录
RUN mkdir -p logs data && chmod 777 logs data

# 暴露端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=5)"

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 部署方式

### 方式一：Docker Compose（推荐）

适合大多数场景，包括开发、测试和生产环境。

#### 启动服务

```bash
# 前台运行（查看日志）
docker compose up

# 后台运行
docker compose up -d

# 构建并启动
docker compose up -d --build

# 强制重新构建
docker compose up -d --build --force-recreate
```

#### 停止服务

```bash
# 停止容器
docker compose stop

# 停止并删除容器
docker compose down

# 停止并删除容器、网络、卷
docker compose down -v
```

#### 查看信息

```bash
# 查看容器状态
docker compose ps

# 查看实时日志
docker compose logs -f

# 查看最近 100 行日志
docker compose logs --tail 100

# 查看特定服务的日志
docker compose logs -f ocs-tiku
```

---

### 方式二：Docker CLI

适合需要精细控制容器行为的场景。

#### 1. 构建镜像

```bash
# 构建镜像
docker build -t ocs-tiku:latest .

# 查看镜像
docker images | grep ocs-tiku
```

#### 2. 运行容器

```bash
docker run -d \
  --name ocs-tiku \
  -p 8000:8000 \
  -v $(pwd)/config.json:/app/config.json:ro \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e TZ=Asia/Shanghai \
  --restart unless-stopped \
  ocs-tiku:latest
```

**参数说明**:
- `-d`: 后台运行
- `--name`: 容器名称
- `-p`: 端口映射
- `-v`: 卷挂载
- `-e`: 环境变量
- `--restart`: 重启策略

#### 3. 管理容器

```bash
# 查看运行中的容器
docker ps

# 查看所有容器（包括已停止）
docker ps -a

# 查看容器日志
docker logs -f ocs-tiku

# 进入容器
docker exec -it ocs-tiku /bin/bash

# 重启容器
docker restart ocs-tiku

# 停止容器
docker stop ocs-tiku

# 删除容器
docker rm ocs-tiku
```

---

### 方式三：多容器部署（含 Redis）

适合生产环境，添加 Redis 缓存支持。

#### 1. 创建 docker-compose.prod.yml

```yaml
version: '3.8'

services:
  # Redis 缓存
  redis:
    image: redis:7-alpine
    container_name: ocs-tiku-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # 应用服务
  ocs-tiku:
    build: .
    image: ocs-tiku:latest
    container_name: ocs-tiku
    ports:
      - "8000:8000"
    volumes:
      - ./config.json:/app/config.json:ro
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      redis:
        condition: service_healthy
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
      - REDIS_URL=redis://redis:6379/0

volumes:
  redis-data:
```

#### 2. 修改 config.json

```json
{
  "cache": {
    "type": "redis",
    "redis_url": "redis://redis:6379/0",
    "ttl": 3600
  }
}
```

#### 3. 启动服务

```bash
# 使用生产配置启动
docker compose -f docker-compose.prod.yml up -d

# 查看服务状态
docker compose -f docker-compose.prod.yml ps
```

---

## 管理与监控

### 1. 容器管理

#### 查看资源使用

```bash
# 查看容器资源占用
docker stats ocs-tiku

# 查看详细信息
docker inspect ocs-tiku
```

#### 限制资源使用

修改 `docker-compose.yml`:

```yaml
services:
  ocs-tiku:
    # ... 其他配置
    deploy:
      resources:
        limits:
          cpus: '1'        # 最多使用 1 个 CPU 核心
          memory: 512M     # 最多使用 512MB 内存
        reservations:
          cpus: '0.5'      # 预留 0.5 个 CPU 核心
          memory: 256M     # 预留 256MB 内存
```

### 2. 日志管理

#### 查看日志

```bash
# 实时日志
docker compose logs -f

# 带时间戳的日志
docker compose logs -f --timestamps

# 最近 100 行
docker compose logs --tail 100

# 持续监控并过滤
docker compose logs -f | grep "ERROR"
```

#### 日志轮转

修改 `docker-compose.yml`:

```yaml
services:
  ocs-tiku:
    # ... 其他配置
    logging:
      driver: "json-file"
      options:
        max-size: "10m"    # 单个日志文件最大 10MB
        max-file: "3"      # 最多保留 3 个日志文件
```

### 3. 性能监控

#### 使用健康检查

健康检查已在 Dockerfile 中配置，可以通过以下方式查看：

```bash
# 查看健康状态
docker inspect --format='{{.State.Health.Status}}' ocs-tiku

# 查看健康检查日志
docker inspect --format='{{json .State.Health}}' ocs-tiku | jq
```

#### 监控 API

访问健康检查端点：

```bash
# 简单健康检查
curl http://localhost:8000/health

# 带详细信息的健康检查（如果实现了）
curl http://localhost:8000/health/detailed
```

---

## 常见问题排查

### 1. 容器启动失败

#### 问题：容器无法启动

**排查步骤**:

```bash
# 查看容器日志
docker compose logs

# 查看容器状态
docker compose ps -a

# 检查配置文件语法
docker compose config

# 尝试前台运行查看详细错误
docker compose up
```

**常见原因**:
- 端口被占用：修改 `docker-compose.yml` 中的端口映射
- 配置文件错误：检查 `config.json` 语法
- 权限问题：确保 `data` 和 `logs` 目录权限正确

### 2. 数据库连接失败

#### 问题：`unable to open database file`

**解决方案**:

```bash
# 1. 检查目录是否存在
ls -la data/

# 2. 修复权限
chmod 777 data logs

# 3. 检查容器内路径
docker exec -it ocs-tiku ls -la /app/data

# 4. 验证配置
docker exec -it ocs-tiku cat /app/config.json | grep database
```

**确保 `config.json` 中的路径**:
```json
{
  "database": {
    "url": "sqlite+aiosqlite:////app/data/question_bank.db"
  }
}
```

### 3. AI 调用失败

#### 问题：AI 服务返回 500 错误

**排查步骤**:

```bash
# 1. 检查配置
docker exec -it ocs-tiku cat /app/config.json | grep -A 20 '"ai"'

# 2. 测试网络连接
docker exec -it ocs-tiku curl -I https://api.siliconflow.cn

# 3. 查看详细日志
docker compose logs | grep -i "ai\|error"

# 4. 验证 API Key
docker exec -it ocs-tiku cat /app/config.json | grep "api_key"
```

**常见原因**:
- API Key 配置错误或过期
- 网络连接问题
- AI 服务商配额用尽
- 配置文件格式错误

### 4. 配置修改不生效

#### 问题：修改 `config.json` 后配置未加载

**解决方案**:

```bash
# 重启容器
docker compose restart

# 或重建容器
docker compose up -d --force-recreate

# 验证配置已加载
docker exec -it ocs-tiku cat /app/config.json
```

### 5. 端口冲突

#### 问题：`port is already allocated`

**解决方案**:

修改 `docker-compose.yml` 中的端口映射：

```yaml
ports:
  - "8080:8000"  # 使用宿主机 8080 端口
```

或停止占用 8000 端口的进程：

```bash
# Linux/macOS
sudo lsof -i :8000
sudo kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 6. 容器无响应

#### 问题：容器运行但无法访问

**排查步骤**:

```bash
# 1. 检查容器状态
docker compose ps

# 2. 检查健康状态
docker inspect --format='{{.State.Health.Status}}' ocs-tiku

# 3. 进入容器检查
docker exec -it ocs-tiku /bin/bash
ps aux  # 查看进程
netstat -tlnp  # 查看监听端口（如果安装了 net-tools）

# 4. 测试内部访问
docker exec -it ocs-tiku curl http://localhost:8000/health
```

### 7. 磁盘空间不足

#### 问题：容器因磁盘空间不足无法启动

**解决方案**:

```bash
# 清理未使用的镜像
docker image prune -a

# 清理未使用的容器
docker container prune

# 清理未使用的卷
docker volume prune

# 清理所有未使用资源
docker system prune -a --volumes

# 查看 Docker 占用空间
docker system df
```

---

## 生产环境优化

### 1. 性能优化

#### 使用 Gunicorn 多进程

修改 Dockerfile 中的启动命令：

```dockerfile
# 安装 gunicorn
RUN pip install gunicorn

# 使用 gunicorn 启动
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

#### 启用 Nginx 反向代理

创建 `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream ocs_tiku {
        server ocs-tiku:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        client_max_body_size 10M;

        location / {
            proxy_pass http://ocs_tiku;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /health {
            proxy_pass http://ocs_tiku/health;
            access_log off;
        }
    }
}
```

修改 `docker-compose.yml` 添加 Nginx：

```yaml
services:
  nginx:
    image: nginx:alpine
    container_name: ocs-tiku-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - ocs-tiku
    restart: unless-stopped

  ocs-tiku:
    # ... 原有配置
    # 不需要暴露端口到宿主机
    expose:
      - "8000"
```

### 2. 环境变量管理

创建 `.env` 文件：

```env
# 应用配置
APP_NAME=OCS题库系统
APP_DEBUG=false

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# AI 服务
AI_DEFAULT_PROVIDER=siliconflow
AI_TIMEOUT=30
AI_MAX_RETRIES=3

# 时区
TZ=Asia/Shanghai

# 版本
VERSION=2.0.0
```

在 `docker-compose.yml` 中使用：

```yaml
services:
  ocs-tiku:
    # ... 其他配置
    env_file:
      - .env
    environment:
      - TZ=${TZ}
```

### 3. 日志聚合

#### 使用 ELK Stack

```yaml
# docker-compose.elk.yml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf:ro
    depends_on:
      - elasticsearch
    ports:
      - "5044:5044"

  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200

volumes:
  elasticsearch-data:
```

### 4. 自动重启策略

在 `docker-compose.yml` 中配置：

```yaml
services:
  ocs-tiku:
    restart: unless-stopped  # 推荐用于生产环境
    # 其他选项：
    # restart: no            # 不自动重启
    # restart: always        # 总是重启（包括手动停止）
    # restart: on-failure    # 失败时重启
    # restart: on-failure:5  # 失败时重启，最多5次
```

---

## 安全最佳实践

### 1. 最小权限原则

#### 使用非 root 用户运行

修改 Dockerfile：

```dockerfile
# 创建专用用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# 后续命令都以 appuser 身份运行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. 敏感信息管理

#### 使用 Docker Secrets

创建 `docker-compose.secrets.yml`:

```yaml
version: '3.8'

services:
  ocs-tiku:
    # ... 其他配置
    secrets:
      - ai_api_key
    environment:
      - AI_API_KEY_FILE=/run/secrets/ai_api_key

secrets:
  ai_api_key:
    file: ./secrets/ai_api_key.txt
```

创建密钥文件：

```bash
mkdir -p secrets
echo "your-actual-api-key" > secrets/ai_api_key.txt
chmod 600 secrets/ai_api_key.txt
```

### 3. 网络隔离

创建独立的网络：

```yaml
version: '3.8'

services:
  ocs-tiku:
    networks:
      - frontend
      - backend
    # ... 其他配置

  redis:
    networks:
      - backend
    # ... 其他配置

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # 内部网络，无法访问外网
```

### 4. 只读根文件系统

```yaml
services:
  ocs-tiku:
    # ... 其他配置
    read_only: true
    tmpfs:
      - /tmp
      - /app/logs
      - /app/data
```

### 5. 镜像安全扫描

```bash
# 使用 Trivy 扫描镜像
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    aquasec/trivy image ocs-tiku:latest

# 或使用 Docker 内置扫描
docker scout cves ocs-tiku:latest
```

---

## 备份与恢复

### 1. 数据备份

#### 备份数据库

```bash
# 创建备份目录
mkdir -p backups

# 备份数据库
docker cp ocs-tiku:/app/data/question_bank.db ./backups/question_bank_$(date +%Y%m%d_%H%M%S).db

# 或使用 tar 打包
tar czf ./backups/ocs-tiku-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
    data/ logs/ config.json
```

#### 自动备份脚本

创建 `scripts/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/ocs-tiku-backup-$TIMESTAMP.tar.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据
tar czf $BACKUP_FILE data/ logs/ config.json

# 删除 7 天前的备份
find $BACKUP_DIR -name "ocs-tiku-backup-*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE"
```

添加到 crontab：

```bash
# 每天凌晨 2 点备份
0 2 * * * /path/to/ocs-tiku/scripts/backup.sh >> /var/log/ocs-backup.log 2>&1
```

### 2. 数据恢复

```bash
# 停止容器
docker compose down

# 恢复数据
tar xzf ./backups/ocs-tiku-backup-20240101_020000.tar.gz

# 重启容器
docker compose up -d
```

### 3. 迁移到新服务器

```bash
# 在旧服务器上打包
tar czf ocs-tiku-migration.tar.gz \
    . \
    --exclude='data' \
    --exclude='logs' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc'

# 传输到新服务器
scp ocs-tiku-migration.tar.gz user@new-server:/path/to/

# 在新服务器上解压
cd /path/to
tar xzf ocs-tiku-migration.tar.gz
cd ocs-tiku

# 单独传输数据和日志
rsync -avz old-server:/path/to/ocs-tiku/data/ ./data/
rsync -avz old-server:/path/to/ocs-tiku/logs/ ./logs/

# 启动服务
docker compose up -d
```

---

## 更新与升级

### 1. 更新应用代码

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker compose up -d --build

# 查看更新日志
docker compose logs -f
```

### 2. 回滚到旧版本

```bash
# 切换到旧版本
git checkout <previous-tag>

# 重新构建
docker compose up -d --build
```

### 3. 零停机更新

使用健康检查和滚动更新：

```bash
# 启动新容器
docker compose up -d --scale ocs-tiku=2 --no-recreate

# 等待新容器健康
sleep 30

# 停止旧容器
docker compose up -d --scale ocs-tiku=1
```

---

## 相关文档

- [安装指南 (INSTALL.md)](./INSTALL.md)
- [API 文档 (API.md)](./API.md)
- [开发指南 (DEVELOPMENT.md)](./DEVELOPMENT.md)

---

**如有问题，请提交 [Issue](https://github.com/wchiways/question-bank/issues)**

