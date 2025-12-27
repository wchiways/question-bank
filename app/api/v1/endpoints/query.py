"""查询端点 - 题库查询API"""
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.api.deps import get_query_service
from app.core.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/query", response_model=QueryResponse, summary="查询问题答案")
async def query_question(
    title: str,
    options: str = "",
    type: str = "single",
    query_service: QueryService = Depends(get_query_service)
):
    """
    查询问题答案

    查询策略:
    1. 首先从缓存查找
    2. 然后从数据库查找
    3. 最后调用AI服务获取

    Args:
        title: 问题标题（必填）
        options: 问题选项
        type: 题目类型 (single/multiple/judgement/fill)
        query_service: 查询服务（依赖注入）

    Returns:
        QueryResponse: 查询响应

    Raises:
        HTTPException: 请求参数错误时抛出400
    """
    try:
        # 构建请求对象
        request = QueryRequest(
            title=title,
            options=options,
            type=type
        )

        # 执行查询
        result = await query_service.query(request)

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
