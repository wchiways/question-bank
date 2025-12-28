"""依赖注入 - FastAPI依赖注入配置"""
from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session_maker
from app.repositories.question_repository import QuestionRepository
from app.repositories.cache_repository import CacheRepository
from app.services.cache_service import CacheService
from app.services.ai_service import AIAsyncService
from app.services.query_service import QueryService
from app.repositories.stats_repository import StatsRepository
from app.repositories.log_repository import LogRepository
from app.repositories.api_key_repository import ApiKeyRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

# 安全配置
security = HTTPBearer(auto_error=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库Session

    Yields:
        AsyncSession: 异步数据库会话
    """
    async with async_session_maker() as session:
        yield session


async def get_question_repo(
    session: AsyncSession = Depends(get_db_session)
) -> QuestionRepository:
    """
    获取QuestionRepository

    Args:
        session: 数据库会话

    Returns:
        QuestionRepository实例
    """
    return QuestionRepository(session)


async def get_cache_repo() -> CacheRepository:
    """
    获取CacheRepository

    Returns:
        CacheRepository实例
    """
    return CacheRepository()


async def get_cache_service(
    cache_repo: CacheRepository = Depends(get_cache_repo)
) -> CacheService:
    """
    获取CacheService

    Args:
        cache_repo: 缓存仓储

    Returns:
        CacheService实例
    """
    return CacheService()


async def get_stats_repo(
    session: AsyncSession = Depends(get_db_session)
) -> StatsRepository:
    """
    获取StatsRepository

    Args:
        session: 数据库会话

    Returns:
        StatsRepository实例
    """
    return StatsRepository(session)


async def get_log_repo(
    session: AsyncSession = Depends(get_db_session)
) -> LogRepository:
    """
    获取LogRepository
    """
    return LogRepository(session)


async def get_api_key_repo(
    session: AsyncSession = Depends(get_db_session)
) -> ApiKeyRepository:
    """
    获取ApiKeyRepository
    """
    return ApiKeyRepository(session)


async def get_ai_service(
    stats_repo: StatsRepository = Depends(get_stats_repo),
    log_repo: LogRepository = Depends(get_log_repo)
) -> AIAsyncService:
    """
    获取AIAsyncService

    Args:
        stats_repo: 统计仓储
        log_repo: 日志仓储

    Returns:
        AIAsyncService实例
    """
    return AIAsyncService(stats_repo=stats_repo, log_repo=log_repo)


async def get_query_service(
    question_repo: QuestionRepository = Depends(get_question_repo),
    cache_service: CacheService = Depends(get_cache_service),
    ai_service: AIAsyncService = Depends(get_ai_service)
) -> QueryService:
    """
    获取QueryService

    Args:
        question_repo: Question仓储
        cache_service: 缓存服务
        ai_service: AI服务

    Returns:
        QueryService实例
    """
    return QueryService(
        question_repo=question_repo,
        cache_service=cache_service,
        ai_service=ai_service
    )


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo)
) -> str:
    """
    验证API密钥

    Args:
        credentials: HTTP Bearer token凭据
        api_key_repo: API密钥仓储

    Returns:
        str: 验证通过的API密钥

    Raises:
        HTTPException: 如果认证失败
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

    api_key = credentials.credentials

    # 查询API密钥是否存在
    key_record = await api_key_repo.find_by_key(api_key)
    if not key_record:
        logger.warning(f"无效的API密钥尝试: {api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的API密钥",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 更新使用统计
    try:
        await api_key_repo.increment_usage(api_key)
    except Exception as e:
        logger.error(f"更新API密钥使用统计失败: {e}")

    logger.info(f"API密钥验证成功: {key_record.name}")
    return api_key
