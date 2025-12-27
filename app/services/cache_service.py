"""缓存服务 - 封装缓存操作"""
from app.repositories.cache_repository import CacheRepository
from app.core.logger import get_logger

logger = get_logger(__name__)


class CacheService:
    """
    缓存服务 - 封装缓存操作
    """

    def __init__(self):
        """初始化缓存服务"""
        self.cache_repo = CacheRepository()

    async def get(self, key: str) -> str | None:
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            缓存值或None
        """
        return await self.cache_repo.get(key)

    async def set(
        self,
        key: str,
        value: str,
        ttl: int | None = None
    ) -> bool:
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间

        Returns:
            成功返回True
        """
        return await self.cache_repo.set(key, value, ttl)

    async def delete(self, key: str) -> bool:
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            成功返回True
        """
        return await self.cache_repo.delete(key)

    async def clear(self) -> bool:
        """
        清空所有缓存

        Returns:
            成功返回True
        """
        return await self.cache_repo.clear()
