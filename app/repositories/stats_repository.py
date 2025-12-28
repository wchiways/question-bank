from typing import Optional
from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stats import ProviderStats
from app.repositories.base import BaseRepository

class StatsRepository(BaseRepository[ProviderStats]):
    """
    统计数据仓储
    """
    def __init__(self, session: AsyncSession):
        super().__init__(ProviderStats, session)

    async def increment_call_count(self, provider_name: str):
        """
        增加调用次数
        """
        statement = select(ProviderStats).where(ProviderStats.provider_name == provider_name)
        result = await self.session.execute(statement)
        stats = result.scalar_one_or_none()

        if stats:
            stats.call_count += 1
            stats.last_called_at = datetime.utcnow()
        else:
            stats = ProviderStats(provider_name=provider_name, call_count=1, last_called_at=datetime.utcnow())
            self.session.add(stats)
        
        await self.session.commit()
        await self.session.refresh(stats)
        return stats

    async def get_all_stats(self):
        """
        获取所有统计数据
        """
        statement = select(ProviderStats)
        result = await self.session.execute(statement)
        return result.scalars().all()
