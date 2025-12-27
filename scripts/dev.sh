#!/bin/bash
# 开发环境启动脚本

set -e

echo "🚀 启动OCS题库系统..."

# 检查配置文件
if [ ! -f config.json ]; then
    echo "⚠️  config.json不存在，从config.example.json创建..."
    cp config.example.json config.json
    echo "✅ config.json已创建，请编辑配置AI API密钥"
    echo "📝 配置指南请查看: docs/配置指南.md"
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "📡 启动FastAPI服务器..."
echo "📖 API文档: http://localhost:8000/docs"
echo "🏥 健康检查: http://localhost:8000/health"
echo ""

uv run uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info
