from typing import List, Optional
from datetime import datetime, timedelta
from sqlmodel import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.log import CallLog
from app.repositories.base import BaseRepository

class LogRepository(BaseRepository[CallLog]):
    """
    日志数据仓储
    """
    def __init__(self, session: AsyncSession):
        super().__init__(CallLog, session)

    async def create_log(
        self,
        provider: str,
        model: str,
        prompt_length: int,
        response_length: int,
        latency_ms: int,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> CallLog:
        log = CallLog(
            provider=provider,
            model=model,
            prompt_length=prompt_length,
            response_length=response_length,
            latency_ms=latency_ms,
            success=success,
            error_message=error_message
        )
        return await self.create(log)

    async def get_logs(self, skip: int = 0, limit: int = 20) -> List[CallLog]:
        """获取分页日志"""
        statement = select(CallLog).order_by(desc(CallLog.created_at)).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_daily_stats(self, days: int = 7):
        """获取最近几天的调用统计"""
        start_date = datetime.utcnow() - timedelta(days=days)
        # SQLite specific date truncation might differ, using generic approach or app logic if complex
        # For simplicity in this demo, fetching and aggregating or using simple grouping
        
        # Note: In SQLite, func.date(CallLog.created_at) works
        statement = select(
            func.date(CallLog.created_at).label("date"),
            func.count(CallLog.id).label("count"),
            func.avg(CallLog.latency_ms).label("avg_latency")
        ).where(
            CallLog.created_at >= start_date
        ).group_by(
            func.date(CallLog.created_at)
        ).order_by("date")
        
        result = await self.session.execute(statement)
        return result.all()
