from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class CallLog(SQLModel, table=True):
    """
    AI调用详细日志
    """
    __tablename__ = "call_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    provider: str = Field(index=True)
    model: str = Field(default="unknown")
    prompt_length: int = Field(default=0)
    response_length: int = Field(default=0)
    latency_ms: int = Field(description="延迟(毫秒)")
    success: bool = Field(default=True)
    error_message: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
