"""查询服务 - 协调数据库、缓存、AI服务的核心业务逻辑"""
from app.repositories.question_repository import QuestionRepository
from app.services.cache_service import CacheService
from app.services.ai_service import AIAsyncService
from app.schemas.query import QueryRequest, QueryResponse
from app.core.logger import get_logger

logger = get_logger(__name__)


class QueryService:
    """
    查询服务 - 协调数据库、缓存、AI服务

    Args:
        question_repo: Question仓储实例
        cache_service: 缓存服务实例
        ai_service: AI异步服务实例
    """

    def __init__(
        self,
        question_repo: QuestionRepository,
        cache_service: CacheService,
        ai_service: AIAsyncService
    ):
        self.question_repo = question_repo
        self.cache_service = cache_service
        self.ai_service = ai_service

    async def query(self, request: QueryRequest) -> QueryResponse:
        """
        查询问题答案

        查询策略:
        1. 尝试从缓存获取
        2. 从数据库查询
        3. 调用AI服务
        4. 保存到数据库和缓存

        Args:
            request: 查询请求

        Returns:
            查询响应
        """
        # 1. 尝试从缓存获取
        cached_answer = await self.cache_service.get(request.title)
        if cached_answer:
            logger.info(f"✅ 缓存命中: {request.title[:50]}...")
            return QueryResponse(
                code=1,
                data=cached_answer,
                msg="缓存命中",
                source="cache"
            )

        # 2. 查询数据库
        db_question = await self.question_repo.find_by_question(request.title)
        if db_question:
            logger.info(f"✅ 数据库命中: {request.title[:50]}...")
            # 更新缓存
            await self.cache_service.set(request.title, db_question.answer)
            return QueryResponse(
                code=1,
                data=db_question.answer,
                msg="本地数据库",
                source="database"
            )

        # 3. 调用AI服务
        logger.info(f"🤖 调用AI服务: {request.title[:50]}...")
        ai_answer = await self.ai_service.get_answer(
            title=request.title,
            options=request.options,
            question_type=request.type.value
        )

        if ai_answer:
            # 保存到数据库
            try:
                await self.question_repo.create_question(
                    question=request.title,
                    answer=ai_answer,
                    options=request.options,
                    question_type=request.type.value
                )
                # 更新缓存
                await self.cache_service.set(request.title, ai_answer)
                logger.info(f"✅ AI答案已保存: {request.title[:50]}...")
            except Exception as e:
                logger.error(f"❌ 保存AI答案失败: {e}")

            return QueryResponse(
                code=1,
                data=ai_answer,
                msg="AI回答",
                source="ai"
            )

        # 4. 未找到答案
        logger.warning(f"❌ 未找到答案: {request.title[:50]}...")
        return QueryResponse(
            code=0,
            data=None,
            msg="未找到答案",
            source="none"
        )
