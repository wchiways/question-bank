"""数据库连接管理 - 异步数据库引擎和Session管理"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# 创建异步引擎
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # 连接健康检查
)

# 创建异步Session工厂
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """
    依赖注入：获取数据库Session

    Yields:
        AsyncSession: 异步数据库会话
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"数据库Session错误: {e}")
            await session.rollback()
            raise


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("✅ 数据库表初始化完成")


async def close_db():
    """关闭数据库连接"""
    await engine.dispose()
    logger.info("✅ 数据库连接已关闭")
