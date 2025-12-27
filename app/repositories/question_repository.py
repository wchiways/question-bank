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
