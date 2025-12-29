# 开发指南

本文档面向开发者，介绍如何参与 OCS 题库系统的开发、项目架构、编码规范和最佳实践。

## 目录

- [开发环境搭建](#开发环境搭建)
- [项目架构](#项目架构)
- [核心模块详解](#核心模块详解)
- [开发流程](#开发流程)
- [编码规范](#编码规范)
- [测试指南](#测试指南)
- [部署指南](#部署指南)
- [常见开发任务](#常见开发任务)

---

## 开发环境搭建

### 前置要求

- Python 3.11+
- Git
- uv (推荐) 或 pip
- IDE: VS Code / PyCharm

### 1. 克隆项目

```bash
git clone https://github.com/wchiways/question-bank.git
cd ocs-tiku
```

### 2. 创建虚拟环境

#### 使用 uv（推荐）

```bash
uv sync
```

#### 使用 pip

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate     # Windows

pip install -e ".[dev]"
```

### 3. 配置开发环境

```bash
# 复制配置文件
cp config.example.json config.json

# 编辑配置，设置 debug 模式
```

编辑 `config.json`:

```json
{
  "app": {
    "debug": true
  },
  "database": {
    "echo": true
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### 4. IDE 配置

#### VS Code

安装推荐扩展：

- Python
- Pylance
- Black Formatter
- Ruff

创建 `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### PyCharm

1. 打开项目
2. Settings → Project → Python Interpreter
3. 选择项目的虚拟环境 (`.venv`)
4. Settings → Tools → Black → 启用 Black
5. Settings → Editor → Code Style → Python → 设置 line length = 100

### 5. 验证环境

```bash
# 运行测试
uv run pytest tests/ -v

# 启动开发服务器
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 访问健康检查
curl http://localhost:8000/health
```

---

## 项目架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                         │
│              (浏览器 / 油猴脚本 / 其他应用)               │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    API Layer                             │
│         FastAPI Routes (app/api/v1/endpoints/)           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Service Layer                          │
│      Business Logic (app/services/)                      │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐    │
│  │  Query   │  │   Cache  │  │        AI          │    │
│  │ Service  │  │  Service │  │     Service        │    │
│  └──────────┘  └──────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 Repository Layer                         │
│      Data Access (app/repositories/)                     │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  Question        │  │     Cache        │            │
│  │  Repository      │  │     Repository   │            │
│  └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   SQLite     │  │    Memory    │  │  External    │  │
│  │  Database    │  │    Cache     │  │   AI APIs    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 分层说明

#### 1. API Layer (API 层)

**职责**:
- 接收 HTTP 请求
- 参数验证
- 调用服务层
- 返回响应

**目录**: `app/api/`

```
app/api/
├── deps.py           # 依赖注入
└── v1/
    ├── router.py     # 路由聚合
    └── endpoints/
        ├── query.py  # 查询端点
        └── health.py # 健康检查
```

#### 2. Service Layer (服务层)

**职责**:
- 业务逻辑
- 协调多个仓储
- 事务管理
- 缓存策略

**目录**: `app/services/`

```
app/services/
├── query_service.py  # 查询服务（核心业务）
├── cache_service.py  # 缓存服务
└── ai_service.py     # AI 服务
```

#### 3. Repository Layer (仓储层)

**职责**:
- 数据访问
- SQL 查询
- 缓存读写

**目录**: `app/repositories/`

```
app/repositories/
└── question_repository.py  # 问题仓储
```

#### 4. Model Layer (模型层)

**职责**:
- 数据模型定义
- 数据库表结构

**目录**: `app/models/`

```
app/models/
└── question.py  # 问题模型
```

#### 5. Schema Layer (Schema 层)

**职责**:
- Pydantic 模型
- 请求/响应验证

**目录**: `app/schemas/`

```
app/schemas/
└── query.py  # 查询相关 Schema
```

#### 6. Provider Layer (提供商层)

**职责**:
- 外部服务集成
- AI 平台适配

**目录**: `app/providers/`

```
app/providers/
├── base.py           # 基类
├── siliconflow.py    # 硅基流动
├── ali_bailian.py    # 阿里百炼
├── zhipu.py          # 智谱AI
├── google.py         # Google
├── openai.py         # OpenAI
└── volcengine.py     # 火山引擎
```

---

## 核心模块详解

### 1. 查询服务 (QueryService)

**位置**: `app/services/query_service.py`

**职责**: 实现三级缓存查询策略

**查询流程**:

```python
async def query(self, request: QueryRequest) -> QueryResponse:
    # 1️⃣ 缓存查询 (最快)
    cached_answer = await self.cache_service.get(request.title)
    if cached_answer:
        return QueryResponse(source="cache", ...)

    # 2️⃣ 数据库查询 (快)
    db_question = await self.question_repo.find_by_question(request.title)
    if db_question:
        await self.cache_service.set(request.title, db_question.answer)
        return QueryResponse(source="database", ...)

    # 3️⃣ AI 服务 (较慢)
    ai_answer = await self.ai_service.get_answer(...)
    if ai_answer:
        await self.question_repo.create_question(...)
        await self.cache_service.set(request.title, ai_answer)
        return QueryResponse(source="ai", ...)

    # 4️⃣ 未找到
    return QueryResponse(source="none", ...)
```

### 2. AI 服务 (AIAsyncService)

**位置**: `app/services/ai_service.py`

**职责**: 统一的 AI 服务调用接口，支持多提供商

**关键方法**:

```python
async def get_answer(
    self,
    title: str,
    options: str,
    question_type: str
) -> Optional[str]:
    """
    调用 AI 服务获取答案

    功能:
    - 自动选择启用的 AI 提供商
    - 失败自动重试
    - 超时控制
    - 多提供商降级
    """
```

**提供商选择逻辑**:

1. 优先使用 `default_provider`
2. 失败时尝试其他启用的提供商
3. 全部失败返回 `None`

### 3. 缓存服务 (CacheService)

**位置**: `app/services/cache_service.py`

**职责**: 内存缓存管理

**实现**:

- 使用 Python 字典作为内存缓存
- 支持 TTL (Time To Live)
- 异步接口

### 4. 问题仓储 (QuestionRepository)

**位置**: `app/repositories/question_repository.py`

**职责**: 数据库操作

**核心方法**:

```python
async def find_by_question(self, question: str) -> Optional[Question]
async def create_question(...) -> Question
async def get_stats() -> Dict[str, int]
```

---

## 开发流程

### 1. 功能开发流程

#### 步骤 1: 需求分析

明确需求：
- 要实现什么功能？
- 涉及哪些模块？
- 需要修改哪些文件？

#### 步骤 2: 创建功能分支

```bash
git checkout -b feature/your-feature-name
```

#### 步骤 3: 编写代码

按照项目架构和编码规范实现功能。

#### 步骤 4: 编写测试

```bash
# 创建测试文件
touch tests/test_your_feature.py

# 编写测试用例
uv run pytest tests/test_your_feature.py -v
```

#### 步骤 5: 代码检查

```bash
# 格式化代码
uv run black app/ tests/

# 代码检查
uv run ruff check app/ tests/

# 类型检查
uv run mypy app/
```

#### 步骤 6: 提交代码

```bash
git add .
git commit -m "feat: add your feature description"

# 推送到远程
git push origin feature/your-feature-name
```

#### 步骤 7: 创建 Pull Request

在 GitHub 上创建 PR，等待代码审查。

### 2. Git 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

#### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具链相关

#### 示例

```bash
# 新功能
git commit -m "feat(query): add fuzzy search support"

# Bug 修复
git commit -m "fix(cache): resolve cache expiration issue"

# 文档
git commit -m "docs(api): update API documentation"

# 重构
git commit -m "refactor(services): simplify query service logic"
```

---

## 编码规范

### 1. Python 代码规范

遵循 [PEP 8](https://pep8.org/) 和项目特定规范。

#### 基本规则

- **行长度**: 最大 100 字符
- **缩进**: 4 空格
- **导入顺序**: stdlib → third-party → local
- **命名规范**:
  - 类名: PascalCase
  - 函数/变量: snake_case
  - 常量: UPPER_CASE
  - 私有成员: _leading_underscore

#### 示例

```python
# ✅ 正确
from typing import Optional
import httpx

from app.core.config import settings
from app.models.question import Question


class QueryService:
    """查询服务"""

    def __init__(self, repository: QuestionRepository):
        self._repository = repository

    async def get_answer(self, question_id: int) -> Optional[str]:
        """获取答案"""
        question = await self._repository.find_by_id(question_id)
        return question.answer if question else None


# ❌ 错误
import sys, os  # 不要一行导入多个
from app.core.config import *  # 不要使用通配符导入
```

### 2. 类型注解

**强制要求**: 所有公共 API 必须有类型注解。

```python
# ✅ 正确
def calculate_score(answers: list[str]) -> float:
    """计算得分"""
    return len(answers) * 10.0


# ❌ 错误
def calculate_score(answers):
    """计算得分"""
    return len(answers) * 10.0
```

### 3. 文档字符串

使用 Google 风格的 docstring。

```python
def query_question(
    title: str,
    options: str = "",
    question_type: str = "single"
) -> QueryResponse:
    """
    查询问题答案

    实现三级缓存策略：
    1. 缓存查询
    2. 数据库查询
    3. AI 服务

    Args:
        title: 问题标题
        options: 问题选项，默认为空
        question_type: 题目类型，默认为单选

    Returns:
        QueryResponse: 查询响应对象

    Raises:
        ValueError: 当标题为空时抛出

    Examples:
        >>> query_question("中国的首都是？", "A.北京 B.上海")
        QueryResponse(code=1, data="A.北京", ...)
    """
    pass
```

### 4. 错误处理

```python
# ✅ 正确：使用自定义异常
class QuestionNotFoundError(Exception):
    """问题未找到异常"""
    pass


# ✅ 正确：捕获特定异常
try:
    result = await service.query(request)
except ValidationError as e:
    logger.warning(f"验证失败: {e}")
    raise HTTPException(status_code=400, detail=str(e))


# ❌ 错误：捕获所有异常
try:
    result = await service.query(request)
except Exception:
    pass  # 吞掉所有错误
```

### 5. 日志规范

```python
from app.core.logger import get_logger

logger = get_logger(__name__)

# ✅ 使用结构化日志
logger.info("用户查询成功", extra={
    "user_id": user.id,
    "question": title[:50],
    "source": "cache"
})

# ✅ 使用日志级别
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.critical("严重错误")

# ❌ 不要使用 print
print("Debug info")  # 错误
```

---

## 测试指南

### 1. 测试结构

```
tests/
├── conftest.py          # pytest 配置和 fixtures
├── test_api/            # API 测试
│   ├── test_query.py
│   └── test_health.py
├── test_services/       # 服务测试
│   ├── test_query_service.py
│   └── test_cache_service.py
└── test_repositories/   # 仓储测试
    └── test_question_repository.py
```

### 2. 编写测试

#### 示例：测试查询端点

```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_query_with_valid_title():
    """测试有效的标题查询"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/query",
            params={
                "title": "测试问题",
                "options": "A. 选项1 B. 选项2"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 1
        assert "data" in data


@pytest.mark.asyncio
async def test_query_with_empty_title():
    """测试空标题"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/query",
            params={"title": ""}
        )

        assert response.status_code == 400
```

### 3. 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定文件
uv run pytest tests/test_api/test_query.py

# 显示详细输出
uv run pytest -v

# 显示打印输出
uv run pytest -s

# 运行覆盖率测试
uv run pytest --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 4. Fixtures

在 `tests/conftest.py` 中定义共享 fixtures：

```python
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """异步 HTTP 客户端"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_question():
    """示例问题数据"""
    return {
        "title": "测试问题",
        "options": "A. 选项1 B. 选项2",
        "type": "single"
    }
```

---

## 部署指南

### 1. 本地开发部署

```bash
# 启动开发服务器
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 生产部署

#### 使用 Gunicorn

```bash
# 安装 gunicorn
pip install gunicorn

# 启动服务
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -
```

#### 使用 systemd

创建 `/etc/systemd/system/ocs-tiku.service`:

```ini
[Unit]
Description=OCS Question Bank System
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/ocs-tiku
Environment="PATH=/path/to/ocs-tiku/.venv/bin"
ExecStart=/path/to/ocs-tiku/.venv/bin/gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile /var/log/ocs-tiku/access.log \
    --error-logfile /var/log/ocs-tiku/error.log
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start ocs-tiku
sudo systemctl enable ocs-tiku
```

### 3. Docker 部署

参考 [Docker 部署指南 (DOCKER.md)](./DOCKER.md)

---

## 常见开发任务

### 1. 添加新的 API 端点

#### 步骤 1: 定义 Schema

在 `app/schemas/` 中创建：

```python
# app/schemas/stats.py
from pydantic import BaseModel


class StatsResponse(BaseModel):
    """统计响应"""
    total_questions: int
    cache_hits: int
    ai_queries: int
```

#### 步骤 2: 创建端点

在 `app/api/v1/endpoints/` 中创建：

```python
# app/api/v1/endpoints/stats.py
from fastapi import APIRouter
from app.schemas.stats import StatsResponse

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """获取系统统计"""
    return StatsResponse(
        total_questions=1000,
        cache_hits=500,
        ai_queries=300
    )
```

#### 步骤 3: 注册路由

在 `app/api/v1/router.py` 中注册：

```python
from app.api.v1.endpoints import stats

api_router.include_router(stats.router, tags=["统计"])
```

### 2. 添加新的 AI 提供商

#### 步骤 1: 创建提供商类

```python
# app/providers/new_provider.py
from app.providers.base import BaseAIProvider


class NewProvider(BaseAIProvider):
    """新 AI 提供商"""

    def __init__(self, api_key: str, model: str):
        super().__init__(api_key, model)
        self.api_url = "https://api.newprovider.com/v1/chat"

    async def _call_api(self, prompt: str) -> Optional[str]:
        """调用 API"""
        # 实现具体的 API 调用逻辑
        pass
```

#### 步骤 2: 注册提供商

在 `app/providers/__init__.py` 中添加：

```python
from .new_provider import NewProvider

PROVIDER_MAP = {
    "siliconflow": SiliconFlowProvider,
    "new_provider": NewProvider,
    # ...
}
```

#### 步骤 3: 配置

在 `config.json` 中添加配置：

```json
{
  "ai": {
    "providers": {
      "new_provider": {
        "enabled": true,
        "api_key": "YOUR_API_KEY",
        "model": "model-name"
      }
    }
  }
}
```

### 3. 添加新的缓存后端

#### 步骤 1: 实现 Redis 缓存

```python
# app/services/redis_cache.py
import redis.asyncio as redis
from app.services.cache_service import CacheService


class RedisCacheService(CacheService):
    """Redis 缓存服务"""

    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl

    async def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        value = await self.redis.get(key)
        return value.decode() if value else None

    async def set(self, key: str, value: str) -> None:
        """设置缓存"""
        await self.redis.setex(key, self.ttl, value)
```

#### 步骤 2: 修改配置

```json
{
  "cache": {
    "type": "redis",
    "redis_url": "redis://localhost:6379/0",
    "ttl": 3600
  }
}
```

### 4. 性能优化

#### 数据库优化

```python
# 添加索引
CREATE INDEX idx_question ON questions(question);

# 使用连接池
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    database_url,
    pool_size=20,
    max_overflow=0
)
```

#### 缓存优化

```python
# 使用更快的缓存
from functools import lru_cache

@lru_cache(maxsize=1000)
def parse_options(options: str) -> list[str]:
    """解析选项（带缓存）"""
    return options.split()
```

---

## 相关文档

- [安装指南 (INSTALL.md)](./INSTALL.md)
- [API 文档 (API.md)](./API.md)
- [Docker 部署 (DOCKER.md)](./DOCKER.md)

---

**祝开发愉快！** 🚀
