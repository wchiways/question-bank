"""Question数据模型 - SQLModel定义"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Text
from sqlalchemy import Index


class QuestionBase(SQLModel):
    """Question基础模型"""
    question: str = Field(index=True, max_length=500, description="问题文本")
    answer: str = Field(description="答案文本")
    options: Optional[str] = Field(
        default="",
        sa_column=Column(Text),
        description="选项内容"
    )
    type: Optional[str] = Field(default="", max_length=50, description="题目类型")


class Question(QuestionBase, table=True):
    """
    Question数据库表模型

    Attributes:
        id: 主键ID
        question: 问题文本（已索引）
        answer: 答案文本
        options: 选项内容
        type: 题目类型
        created_at: 创建时间
    """
    __tablename__ = "question_answer"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 定义复合索引
    __table_args__ = (
        Index("idx_question_type", "question", "type"),
    )

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "options": self.options,
            "type": self.type,
            "created_at": self.created_at.isoformat()
        }


class QuestionCreate(QuestionBase):
    """创建Question的请求模型"""
    pass


class QuestionRead(QuestionBase):
    """读取Question的响应模型"""
    id: int
    created_at: datetime


class QuestionUpdate(SQLModel):
    """更新Question的请求模型"""
    answer: Optional[str] = None
    options: Optional[str] = None
    type: Optional[str] = None
