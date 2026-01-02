"""Redis连接管理 - 异步Redis客户端"""
from redis.asyncio import Redis
from typing import Optional
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class RedisManager:
    """Redis连接管理器"""

    def __init__(self):
        self._redis: Optional[Redis] = None

    async def get_redis(self) -> Redis:
        """
        获取Redis客户端实例（单例模式）

        Returns:
            Redis客户端实例
        """
        if self._redis is None:
            await self.connect()
        return self._redis

    async def connect(self) -> None:
        """创建Redis连接"""
        try:
            self._redis = Redis(
                host=settings.cache.host,
                port=settings.cache.port,
                db=settings.cache.db,
                password=settings.cache.password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
            )
            # 测试连接
            await self._redis.ping()
            logger.info("✅ Redis连接成功")
        except Exception as e:
            logger.warning(f"⚠️  Redis连接失败: {e}")
            logger.info("将使用内存缓存替代Redis")
            self._redis = None

    async def close(self) -> None:
        """关闭Redis连接"""
        if self._redis:
            await self._redis.close()
            self._redis = None
            logger.info("✅ Redis连接已关闭")

    async def ping(self) -> bool:
        """测试Redis连接是否正常"""
        try:
            if self._redis:
                await self._redis.ping()
                return True
        except Exception as e:
            logger.warning(f"Redis ping失败: {e}")
            self._redis = None
        return False


# 全局Redis管理器实例
redis_manager = RedisManager()
