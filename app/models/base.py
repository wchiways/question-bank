"""基础模型类定义"""
from sqlmodel import SQLModel


class Base(SQLModel):
    """所有模型的基类"""

    class Config:
        """Pydantic配置"""
        from_attributes = True  # 允许从ORM对象创建
        json_schema_extra = {
            "example": {}
        }
