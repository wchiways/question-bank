"""缓存仓储 - 支持内存和Redis缓存"""
from typing import Optional
from app.core.config import settings
from app.core.redis import redis_manager
from app.core.logger import get_logger

logger = get_logger(__name__)


class CacheRepository:
    """
    缓存仓储 - 支持内存和Redis

    根据配置自动选择缓存后端
    """

    def __init__(self):
        self._memory_cache: dict = {}
        self._cache_type = settings.cache.type.lower()
        self._ttl = settings.cache.ttl
        self._redis = None

    async def _get_redis(self):
        """获取Redis客户端"""
        if self._cache_type == "redis" and self._redis is None:
            self._redis = await redis_manager.get_redis()
        return self._redis

    async def get(self, key: str) -> Optional[str]:
        """
        获取缓存

        Args:
            key: 缓存键

        Returns:
            缓存值或None
        """
        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis:
                    value = await redis.get(key)
                    if value:
                        logger.debug(f"✅ Redis缓存命中: {key[:50]}...")
                    return value
            except Exception as e:
                logger.warning(f"⚠️  Redis读取失败: {e}，降级到内存缓存")

        # 内存缓存（或Redis失败时的降级方案）
        return self._memory_cache.get(key)

    async def set(
        self,
        key: str,
        value: str,
        ttl: Optional[int] = None
    ) -> bool:
        """
        设置缓存

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒）

        Returns:
            成功返回True
        """
        ttl = ttl or self._ttl

        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis:
                    await redis.setex(key, ttl, value)
                    logger.debug(f"📝 Redis缓存已设置: {key[:50]}...")
                    # 同时设置内存缓存作为备份
                    self._memory_cache[key] = value
                    return True
            except Exception as e:
                logger.warning(f"⚠️  Redis写入失败: {e}，使用内存缓存")

        # 内存缓存
        self._memory_cache[key] = value
        logger.debug(f"📝 内存缓存已设置: {key[:50]}...")
        return True

    async def delete(self, key: str) -> bool:
        """
        删除缓存

        Args:
            key: 缓存键

        Returns:
            成功返回True
        """
        success = False

        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis:
                    result = await redis.delete(key)
                    if result:
                        logger.debug(f"🗑️  Redis缓存已删除: {key[:50]}...")
                        success = True
            except Exception as e:
                logger.warning(f"⚠️  Redis删除失败: {e}")

        # 同时删除内存缓存
        if key in self._memory_cache:
            del self._memory_cache[key]
            logger.debug(f"🗑️  内存缓存已删除: {key[:50]}...")
            success = True

        return success

    async def clear(self) -> bool:
        """
        清空所有缓存

        Returns:
            成功返回True
        """
        success = False

        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis:
                    await redis.flushdb()
                    logger.info("🧹 Redis缓存已清空")
                    success = True
            except Exception as e:
                logger.warning(f"⚠️  Redis清空失败: {e}")

        # 清空内存缓存
        self._memory_cache.clear()
        logger.info("🧹 内存缓存已清空")
        success = True

        return success

    async def exists(self, key: str) -> bool:
        """
        检查缓存是否存在

        Args:
            key: 缓存键

        Returns:
            存在返回True
        """
        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis:
                    return await redis.exists(key) > 0
            except Exception as e:
                logger.warning(f"⚠️  Redis检查失败: {e}")

        return key in self._memory_cache

    async def expire(self, key: str, ttl: int) -> bool:
        """
        设置缓存过期时间

        Args:
            key: 缓存键
            ttl: 过期时间（秒）

        Returns:
            成功返回True
        """
        if self._cache_type == "redis":
            try:
                redis = await self._get_redis()
                if redis and await redis.exists(key):
                    await redis.expire(key, ttl)
                    return True
            except Exception as e:
                logger.warning(f"⚠️  Redis设置过期时间失败: {e}")

        # 内存缓存暂不支持TTL，返回True避免阻塞
        return True
