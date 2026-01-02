# 数据库使用指南

本项目使用 SQLAlchemy + SQLModel 进行数据库操作，支持异步和同步两种模式。

## 📊 数据库配置

### 数据库文件位置
- 开发环境: `./question_bank.db`
- 支持的数据库: SQLite（默认）、PostgreSQL、MySQL

### 配置文件
```python
# config.json
{
  "database": {
    "url": "sqlite+aiosqlite:///./question_bank.db",
    "echo": false
  }
}
```

## 🔧 基础操作

### 1. 数据库模型

```python
from app.models.question import Question

# Question 模型字段:
# - id: 主键
# - question: 问题文本
# - answer: 答案文本
# - options: 选项内容
# - type: 题目类型 (single/multiple/judgement/fill/essay)
# - created_at: 创建时间
```

### 2. 创建数据库会话

```python
from app.core.database import get_session

# 异步操作
async for session in get_session():
    # 执行数据库操作
    pass
```

## 📝 CRUD 操作示例

### 创建 (Create)

```python
from app.repositories.question_repository import QuestionRepository

async def create_example():
    async for session in get_session():
        repo = QuestionRepository(session)

        # 方法1: 使用 Repository 方法
        question = await repo.create_question(
            question="你的问题",
            answer="答案内容",
            options="选项A\n选项B\n选项C",
            question_type="single"
        )

        # 方法2: 直接创建模型
        from app.models.question import Question
        new_question = Question(
            question="问题2",
            answer="答案2",
            type="judgement"
        )
        await repo.create(new_question)
```

### 读取 (Read)

```python
from sqlalchemy import select

async def query_examples():
    async for session in get_session():
        repo = QuestionRepository(session)

        # 1. 查询所有题目
        statement = select(Question)
        result = await session.execute(statement)
        all_questions = result.scalars().all()

        # 2. 根据问题查找
        question = await repo.find_by_question("问题内容")

        # 3. 根据类型查找
        statement = select(Question).where(Question.type == "single")
        result = await session.execute(statement)
        single_choice = result.scalars().all()

        # 4. 模糊搜索
        statement = select(Question).where(
            Question.question.contains("关键词")
        )
        result = await session.execute(statement)
        search_results = result.scalars().all()
```

### 更新 (Update)

```python
async def update_example():
    async for session in get_session():
        repo = QuestionRepository(session)

        # 1. 查找要更新的记录
        question = await repo.find_by_question("原问题")

        if question:
            # 2. 直接修改字段
            question.answer = "新答案"
            question.options = "新选项"

            # 3. 提交更改
            await session.commit()

            print("更新成功！")
```

### 删除 (Delete)

```python
async def delete_example():
    async for session in get_session():
        repo = QuestionRepository(session)

        # 1. 查找要删除的记录
        question = await repo.find_by_question("要删除的问题")

        if question:
            # 2. 删除记录
            await session.delete(question)

            # 3. 提交更改
            await session.commit()

            print("删除成功！")
```

## 📄 分页查询

```python
async def pagination_example(page: int = 1, page_size: int = 20):
    async for session in get_session():
        repo = QuestionRepository(session)

        # 分页查询
        skip = (page - 1) * page_size

        result = await repo.get_paginated(
            skip=skip,
            limit=page_size,
            keyword=None,      # 可选：搜索关键词
            question_type=None # 可选：题目类型筛选
        )

        print(f"总数: {result['total']}")
        print(f"当前页: {len(result['items'])}")

        for item in result['items']:
            print(f"- {item.question}")
```

## 🔍 高级查询

### 条件查询

```python
from sqlalchemy import and_, or_

async def advanced_query():
    async for session in get_session():
        # 多条件查询
        statement = select(Question).where(
            and_(
                Question.type == "single",
                Question.question.contains("Python")
            )
        )

        # OR 查询
        statement = select(Question).where(
            or_(
                Question.type == "single",
                Question.type == "multiple"
            )
        )

        result = await session.execute(statement)
        questions = result.scalars().all()
```

### 排序和限制

```python
async def sort_limit_example():
    async for session in get_session():
        # 按创建时间倒序
        statement = select(Question).order_by(
            Question.created_at.desc()
        ).limit(10)

        result = await session.execute(statement)
        latest_questions = result.scalars().all()
```

### 统计查询

```python
async def statistics_example():
    async for session in get_session():
        repo = QuestionRepository(session)

        # 统计各类型题目数量
        statement = select(Question.type, func.count(Question.id)).group_by(Question.type)

        result = await session.execute(statement)
        stats = result.all()

        for type_name, count in stats:
            print(f"{type_name}: {count}题")
```

## ⚡ 最佳实践

### 1. 使用 Repository 模式
```python
# ✅ 推荐
async for session in get_session():
    repo = QuestionRepository(session)
    question = await repo.find_by_question("问题")

# ❌ 不推荐
async for session in get_session():
    statement = select(Question).where(Question.question == "问题")
    result = await session.execute(statement)
    question = result.scalar_one_or_none()
```

### 2. 异步上下文管理
```python
# ✅ 正确
async for session in get_session():
    # 操作
    pass

# ❌ 错误
session = get_session()
# 这样无法正确管理资源
```

### 3. 错误处理
```python
async def safe_operation():
    try:
        async for session in get_session():
            repo = QuestionRepository(session)
            # 执行操作
            await session.commit()
    except Exception as e:
        print(f"操作失败: {e}")
        # 自动回滚
```

### 4. 批量操作
```python
async def batch_insert():
    async for session in get_session():
        repo = QuestionRepository(session)

        questions_data = [
            {"question": "Q1", "answer": "A1", "type": "single"},
            {"question": "Q2", "answer": "A2", "type": "single"},
        ]

        for data in questions_data:
            await repo.create_question(**data)

        await session.commit()
```

## 🔒 数据安全

### 敏感数据处理
```python
# API Key 等敏感信息不要存入数据库
# 使用环境变量或配置文件

import os
api_key = os.getenv("OPENAI_API_KEY")
```

### 数据备份
```bash
# 备份数据库
cp question_bank.db question_bank.db.backup

# 或使用 SQLite 命令
sqlite3 question_bank.db ".backup question_bank.db.backup"
```

## 🚀 性能优化

### 索引使用
```python
# 模型中已定义索引
class Question(QuestionBase, table=True):
    __tablename__ = "question_answer"

    # 复合索引
    __table_args__ = (
        Index("idx_question_type", "question", "type"),
    )
```

### 查询优化
```python
# ✅ 使用索引字段
statement = select(Question).where(Question.type == "single")

# ❌ 避免全表扫描
statement = select(Question).where(
    Question.question.contains("%" + keyword + "%")
)
```

## 📚 更多示例

完整示例代码请参考：`docs/database_examples.py`

运行示例：
```bash
cd /home/toniwang/Project/ocs-tiku
python docs/database_examples.py
```

## ❓ 常见问题

### Q: 如何重置数据库？
```bash
rm question_bank.db
# 应用重启时会自动创建
```

### Q: 如何查看数据库内容？
```bash
sqlite3 question_bank.db
.tables
SELECT * FROM question_answer LIMIT 10;
```

### Q: 如何迁移到其他数据库？
修改 `config.json` 中的数据库 URL 即可：
```json
{
  "database": {
    "url": "postgresql://user:password@localhost/dbname"
  }
}
```
