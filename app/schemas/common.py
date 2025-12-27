"""通用Schema定义"""
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """
    通用响应模型

    Args:
        code: 状态码
        msg: 消息
        data: 数据
    """
    code: int
    msg: str
    data: Optional[T] = None
