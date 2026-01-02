"""Question仓储 - 封装题库数据访问逻辑"""
from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.question import Question
from app.repositories.base import BaseRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class QuestionRepository(BaseRepository[Question]):
    """
    Question仓储 - 封装题库数据访问逻辑

    Args:
        session: 异步数据库会话
    """

    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)

    async def find_by_question(self, question: str) -> Optional[Question]:
        """
        根据问题文本查找

        Args:
            question: 问题文本

        Returns:
            Question对象或None
        """
        statement = select(Question).where(Question.question == question)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def find_by_question_type(
        self,
        question: str,
        question_type: str
    ) -> Optional[Question]:
        """
        根据问题和类型查找

        Args:
            question: 问题文本
            question_type: 题目类型

        Returns:
            Question对象或None
        """
        statement = select(Question).where(
            Question.question == question,
            Question.type == question_type
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def exists(self, question: str) -> bool:
        """
        检查问题是否存在

        Args:
            question: 问题文本

        Returns:
            存在返回True
        """
        result = await self.find_by_question(question)
        return result is not None

    async def create_question(
        self,
        question: str,
        answer: str,
        options: str = "",
        question_type: str = ""
    ) -> Question:
        """
        创建新问题

        Args:
            question: 问题文本
            answer: 答案文本
            options: 选项内容
            question_type: 题目类型

        Returns:
            创建的Question对象
        """
        question_obj = Question(
            question=question,
            answer=answer,
            options=options,
            type=question_type
        )
        return await self.create(question_obj)

    async def get_paginated(
        self,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        question_type: Optional[str] = None
    ) -> dict:
        """
        获取分页题目列表（性能优化版本）

        Args:
            skip: 跳过的记录数
            limit: 返回的记录数限制
            keyword: 搜索关键词
            question_type: 题目类型筛选

        Returns:
            包含items、total、page、page_size的字典
        """
        from sqlmodel import func

        # 性能优化：只选择必要的字段
        statement = select(Question.id, Question.question, Question.answer,
                          Question.options, Question.type, Question.created_at)

        # 性能优化：使用更高效的count查询
        count_statement = select(func.count(Question.id))

        # 应用过滤条件
        if keyword:
            # 性能优化：使用索引友好的like查询
            statement = statement.where(Question.question.like(f"%{keyword}%"))
            count_statement = count_statement.where(Question.question.like(f"%{keyword}%"))

        if question_type:
            statement = statement.where(Question.type == question_type)
            count_statement = count_statement.where(Question.type == question_type)

        # 性能优化：先执行count查询（更快）
        total_result = await self.session.execute(count_statement)
        total = total_result.scalar_one()

        # 性能优化：添加排序以确保结果一致性
        statement = statement.order_by(Question.id.desc())

        # 分页查询
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)

        # 性能优化：手动构建对象（避免完整的ORM开销）
        items = []
        for row in result.all():
            items.append(Question(
                id=row[0],
                question=row[1],
                answer=row[2],
                options=row[3],
                type=row[4],
                created_at=row[5]
            ))

        return {
            "items": items,
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "page_size": limit
        }
