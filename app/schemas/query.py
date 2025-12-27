"""查询相关的Pydantic Schema定义"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class QuestionType(str, Enum):
    """题目类型枚举"""
    SINGLE = "single"  # 单选题
    MULTIPLE = "multiple"  # 多选题
    JUDGEMENT = "judgement"  # 判断题
    FILL = "fill"  # 填空题


class QueryRequest(BaseModel):
    """
    查询请求Schema

    Attributes:
        title: 问题标题（必填）
        options: 选项内容
        type: 题目类型
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="问题标题",
        examples=["中国的首都是哪里？"]
    )
    options: str = Field(
        default="",
        max_length=1000,
        description="选项内容",
        examples=["A. 北京 B. 上海 C. 广州"]
    )
    type: QuestionType = Field(
        default=QuestionType.SINGLE,
        description="题目类型"
    )

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """
        验证标题不能为空

        Args:
            v: 标题值

        Returns:
            清理后的标题

        Raises:
            ValueError: 标题为空时抛出
        """
        if not v or not v.strip():
            raise ValueError('标题不能为空')
        return v.strip()

    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "examples": [
                {
                    "title": "中国的首都是哪里？",
                    "options": "A. 北京 B. 上海 C. 广州",
                    "type": "single"
                }
            ]
        }


class QueryResponse(BaseModel):
    """
    查询响应Schema

    Attributes:
        code: 状态码（1-成功，0-失败）
        data: 答案内容
        msg: 响应消息
        source: 答案来源
    """
    code: int = Field(description="状态码: 1-成功, 0-失败")
    data: Optional[str] = Field(None, description="答案内容")
    msg: str = Field(description="响应消息")
    source: str = Field(description="答案来源: cache/database/ai/none")


class ErrorResponse(BaseModel):
    """
    错误响应Schema

    Attributes:
        success: 是否成功（固定为false）
        error: 错误信息
    """
    success: bool = False
    error: str = Field(description="错误信息")
