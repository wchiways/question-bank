from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class ProviderStats(SQLModel, table=True):
    """
    AI提供商调用统计
    """
    __tablename__ = "provider_stats"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_name: str = Field(index=True)
    call_count: int = Field(default=0)
    last_called_at: datetime = Field(default_factory=datetime.utcnow)
