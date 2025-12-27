#!/bin/bash
# 开发环境启动脚本

set -e

echo "🚀 启动OCS题库系统..."

# 检查环境变量
if [ ! -f .env ]; then
    echo "⚠️  .env文件不存在，从.env.example创建..."
    cp .env.example .env
    echo "✅ .env文件已创建，请编辑配置AI_API_KEY"
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "📡 启动FastAPI服务器..."
uv run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info
