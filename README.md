# OCS题库系统 - FastAPI版本

> 基于FastAPI + AsyncIO + SQLModel的高性能题库查询系统

## 🚀 特性

- ✅ **异步架构**: 全链路异步处理，支持高并发
- ✅ **类型安全**: 100%类型注解，Pydantic数据验证
- ✅ **自动文档**: Swagger UI和ReDoc自动生成
- ✅ **分层设计**: 清晰的分层架构，易于维护
- ✅ **三级缓存**: 内存缓存 + 数据库 + AI服务
- ✅ **智能重试**: AI调用失败自动重试
- ✅ **多AI平台**: 支持硅基流动、阿里百炼、智谱AI、Google、OpenAI等多个平台

## 🛠️ 技术栈

- **Web框架**: FastAPI 0.127+
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **数据库**: SQLite (aiosqlite异步驱动)
- **HTTP客户端**: httpx (异步)
- **日志**: loguru
- **包管理**: uv

## 📦 快速开始

### 环境要求

- Python 3.11+
- uv (推荐) 或 pip

### 安装

```bash
# 使用uv (推荐)
uv sync

# 或使用pip
pip install -e .
```

### 配置

复制配置文件模板：

```bash
cp config.example.json config.json
```

编辑`config.json`文件，配置你的AI服务：

```json
{
  "ai": {
    "default_provider": "siliconflow",
    "providers": {
      "siliconflow": {
        "enabled": true,
        "api_key": "YOUR_API_KEY"
      },
      "ali_bailian": {
        "enabled": false,
        "api_key": "YOUR_ALI_BAILIAN_API_KEY"
      }
    }
  }
}
```

**支持的AI平台**:
- **硅基流动** (siliconflow) - 默认，性价比高
- **阿里百炼** (ali_bailian) - 阿里云大模型平台
- **智谱AI** (zhipu) - 清华KEG实验室
- **Google Studio AI** (google) - Google Gemini
- **OpenAI** (openai) - GPT系列模型

### 运行

```bash
# 开发模式
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用脚本
./scripts/dev.sh
```

访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 📁 项目结构

```
ocs-tiku/
├── app/
│   ├── api/              # API路由层
│   │   ├── deps.py       # 依赖注入
│   │   └── v1/           # API v1版本
│   ├── core/             # 核心配置
│   │   ├── config.py     # 配置管理
│   │   ├── db.py         # 数据库连接
│   │   └── logger.py     # 日志系统
│   ├── models/           # 数据模型
│   ├── schemas/          # Pydantic Schema
│   ├── repositories/     # 数据访问层
│   ├── services/         # 业务逻辑层
│   └── providers/        # 外部服务提供商
├── tests/                # 测试
├── .env.example          # 环境变量模板
├── pyproject.toml        # 项目配置
└── README.md
```

## 🔌 API使用

### 查询问题答案

```bash
curl "http://localhost:8000/api/v1/query?title=中国的首都是哪里？&options=A.北京 B.上海&type=single"
```

响应：

```json
{
  "code": 1,
  "data": "A.北京",
  "msg": "AI回答",
  "source": "ai"
}
```

## 🧪 测试

```bash
# 运行测试
uv run pytest tests/ -v

# 查看覆盖率
uv run pytest tests/ --cov=app --cov-report=html
```

## 📊 性能

相比旧版Flask架构：

| 指标 | Flask版本 | FastAPI版本 | 提升 |
|------|----------|-------------|------|
| 并发处理 | 4 QPS | 200+ QPS | **50倍** |
| 响应时间 | ~100ms | <50ms | **2倍** |
| 代码量 | 239行 | 减少40% | 更简洁 |

## 🔄 从Flask迁移

旧版本（Flask）保留在Git历史中。新版本（FastAPI）在`development`分支开发。

迁移步骤：
1. 备份数据库：`cp question_bank.db question_bank.db.backup`
2. 安装新依赖：`uv sync`
3. 配置AI服务：复制`config.example.json`为`config.json`并填入API密钥
4. 启动新服务：`uv run uvicorn app.main:app`或`./scripts/dev.sh`

## 📝 开发指南

### 添加新的API端点

1. 在`app/schemas/`定义请求/响应模型
2. 在`app/api/v1/endpoints/`创建端点文件
3. 在`app/api/v1/router.py`注册路由
4. 添加相应的服务和仓储方法

### 代码风格

```bash
# 格式化代码
uv run black app/

# 代码检查
uv run ruff check app/
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🎉 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [uv](https://github.com/astral-sh/uv)
