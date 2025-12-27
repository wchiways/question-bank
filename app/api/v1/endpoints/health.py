"""健康检查端点 - 系统健康状态API"""
from fastapi import APIRouter
from app.schemas.health import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, summary="健康检查")
async def health_check():
    """
    健康检查端点

    Returns:
        HealthResponse: 健康状态信息
    """
    from app.core.config import settings
    return HealthResponse(
        status="healthy",
        app_name=settings.app.name,
        version=settings.app.version,
        environment="development" if settings.app.debug else "production"
    )
