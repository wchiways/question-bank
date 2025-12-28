"""查询端点 - 题库查询API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.api.deps import get_query_service, get_api_key_repo
from app.repositories.api_key_repository import ApiKeyRepository
from app.utils.helpers import match_option
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/query", response_model=QueryResponse, summary="查询问题答案")
async def query_question(
    title: str,
    key: str = Query(..., description="API密钥"),
    options: str = "",
    type: str = "single",
    query_service: QueryService = Depends(get_query_service),
    api_key_repo: ApiKeyRepository = Depends(get_api_key_repo)
):
    """
    查询问题答案

    需要提供有效的 API Key。
    """
    # 验证 API Key
    api_key = await api_key_repo.find_by_key(key)
    if not api_key or not api_key.enabled:
        logger.warning(f"⚠️ 无效或未启用的 API Key: {key}")
        raise HTTPException(status_code=403, detail="无效的 API 密钥")

    # 记录使用次数 (异步执行，不阻塞)
    await api_key_repo.increment_usage(key)

    try:
        # 构建请求对象
        request = QueryRequest(
            title=title,
            options=options,
            type=type
        )

        # 执行查询
        result = await query_service.query(request)
        
        # 智能答案匹配：如果答案不包含字母前缀，尝试从选项中匹配
        if result.data and result.code == 1 and options:
            matched_answer = match_option(result.data, options)
            if matched_answer != result.data:
                logger.info(f"🎯 智能匹配: '{result.data[:30]}...' -> '{matched_answer}'")
                result.data = matched_answer

        return result

    except ValueError as e:
        logger.warning(f"⚠️ 参数验证失败: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ 查询失败: {e}")
        raise HTTPException(
            status_code=500,
            detail="查询失败，请稍后重试"
        )
