"""
数据库使用示例
演示如何使用项目的数据库功能
"""
import asyncio
from sqlalchemy import select
from app.core.config import config_manager
from app.core.database import get_session
from app.models.question import Question
from app.repositories.question_repository import QuestionRepository


async def example_create_question():
    """示例：创建新题目"""
    print("=== 示例1: 创建新题目 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 创建单选题
        question = await repo.create_question(
            question="Python 是什么类型的编程语言？",
            answer="A. 解释型语言",
            options="A. 解释型语言\nB. 编译型语言\nC. 汇编型语言\nD. 机器语言",
            question_type="single"
        )

        print(f"✅ 创建成功！题目ID: {question.id}")
        print(f"   问题: {question.question}")
        print(f"   答案: {question.answer}")
        print(f"   类型: {question.type}")


async def example_query_questions():
    """示例：查询题目"""
    print("\n=== 示例2: 查询题目 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 查询所有题目
        statement = select(Question)
        result = await session.execute(statement)
        questions = result.scalars().all()

        print(f"📊 题库总数: {len(questions)}")

        # 按类型统计
        type_count = {}
        for q in questions:
            type_count[q.type] = type_count.get(q.type, 0) + 1

        print("\n题目类型分布:")
        for type_name, count in type_count.items():
            print(f"  - {type_name}: {count}题")


async def example_search_question():
    """示例：搜索题目"""
    print("\n=== 示例3: 搜索题目 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 根据关键词搜索
        keyword = "Python"
        statement = select(Question).where(Question.question.contains(keyword))
        result = await session.execute(statement)
        questions = result.scalars().all()

        print(f"🔍 搜索 '{keyword}' 的结果: {len(questions)}条")

        for q in questions[:3]:  # 只显示前3条
            print(f"\n  Q: {q.question[:50]}...")
            print(f"  A: {q.answer}")


async def example_update_question():
    """示例：更新题目"""
    print("\n=== 示例4: 更新题目 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 查找题目
        question = await repo.find_by_question("Python 是什么类型的编程语言？")

        if question:
            # 更新答案
            question.answer = "A. 解释型语言（更新）"
            await session.commit()

            print(f"✅ 更新成功！答案: {question.answer}")


async def example_delete_question():
    """示例：删除题目"""
    print("\n=== 示例5: 删除题目 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 查找题目
        question = await repo.find_by_question("Python 是什么类型的编程语言？")

        if question:
            question_id = question.id
            await session.delete(question)
            await session.commit()

            print(f"✅ 删除成功！题目ID: {question_id}")


async def example_paginated_query():
    """示例：分页查询"""
    print("\n=== 示例6: 分页查询 ===")

    async for session in get_session():
        repo = QuestionRepository(session)

        # 分页查询
        page_size = 10
        page = 1

        result = await repo.get_paginated(
            skip=(page - 1) * page_size,
            limit=page_size
        )

        print(f"📄 第 {page} 页，每页 {page_size} 条")
        print(f"   总数: {result['total']}")
        print(f"   本页: {len(result['items'])} 条")

        # 显示前3条
        for item in result['items'][:3]:
            print(f"   - [{item.type}] {item.question[:30]}...")


async def main():
    """运行所有示例"""
    print("🎯 数据库使用示例\n")

    try:
        # 示例1: 创建题目
        await example_create_question()

        # 示例2: 查询题目
        await example_query_questions()

        # 示例3: 搜索题目
        await example_search_question()

        # 示例4: 更新题目
        await example_update_question()

        # 示例5: 分页查询
        await example_paginated_query()

        # 示例6: 删除题目（可选）
        # await example_delete_question()

        print("\n✅ 所有示例运行完成！")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
