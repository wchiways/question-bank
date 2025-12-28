from typing import List, Optional
from datetime import datetime
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_key import ApiKey
from app.repositories.base import BaseRepository

class ApiKeyRepository(BaseRepository[ApiKey]):
    """
    API密钥仓储
    """
    def __init__(self, session: AsyncSession):
        super().__init__(ApiKey, session)

    async def find_by_key(self, key: str) -> Optional[ApiKey]:
        """根据Key查找"""
        statement = select(ApiKey).where(ApiKey.key == key)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_key(self, key: str, name: str = "Default") -> ApiKey:
        """创建新密钥"""
        api_key = ApiKey(key=key, name=name)
        return await self.create(api_key)

    async def get_all_keys(self) -> List[ApiKey]:
        """获取所有密钥"""
        statement = select(ApiKey).order_by(ApiKey.created_at.desc())
        result = await self.session.execute(statement)
        return result.scalars().all()
    
    async def delete_by_key(self, key: str) -> bool:
        """根据Key删除"""
        api_key = await self.find_by_key(key)
        if api_key:
            await self.session.delete(api_key)
            await self.session.commit()
            return True
        return False

    async def increment_usage(self, key: str):
        """增加使用次数"""
        api_key = await self.find_by_key(key)
        if api_key:
            api_key.usage_count += 1
            api_key.last_used_at = datetime.utcnow()
            self.session.add(api_key)
            await self.session.commit()
