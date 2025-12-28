from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class ApiKey(SQLModel, table=True):
    """
    API密钥模型
    """
    __tablename__ = "api_keys"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True, description="API Key")
    name: str = Field(default="Default", description="密钥名称/备注")
    enabled: bool = Field(default=True, description="是否启用")
    usage_count: int = Field(default=0, description="使用次数")
    last_used_at: Optional[datetime] = Field(default=None, description="最后使用时间")
    created_at: datetime = Field(default_factory=datetime.utcnow)
