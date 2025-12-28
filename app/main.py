"""FastAPI应用主入口 - 应用初始化和路由注册"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.db import init_db, close_db
from app.core.logger import get_logger, setup_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理

    Args:
        app: FastAPI应用实例
    """
    # 启动时执行
    logger.info(f"🚀 {settings.app.name} v{settings.app.version} 启动中...")
    await init_db()
    logger.info("✅ 数据库初始化完成")

    yield

    # 关闭时执行
    logger.info("🛑 应用关闭中...")
    await close_db()
    logger.info("✅ 数据库连接已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description="基于FastAPI + AsyncIO的高性能题库查询系统",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.app.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="app/templates")

# 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.security.allowed_hosts,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# 健康检查端点
@app.get("/health")
async def health_check():
    """
    健康检查端点

    Returns:
        健康状态信息
    """
    return {
        "status": "healthy",
        "app_name": settings.app.name,
        "version": settings.app.version,
        "environment": "development" if settings.app.debug else "production"
    }


# 根路径 - 首页
@app.get("/")
async def root(request: Request):
    """
    网站首页

    Args:
        request: FastAPI请求对象

    Returns:
        首页HTML
    """
    return templates.TemplateResponse("index.html", {"request": request})


# 注册路由
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.app.api_v1_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.app.debug,
        log_level=settings.logging.level.lower(),
    )
