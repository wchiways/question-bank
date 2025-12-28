"""FastAPI应用主入口 - 应用初始化和路由注册"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
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

# 挂载静态文件 (优先挂载 API 之前的路由，或者在 API 之后处理 SPA catch-all)
# 在 Docker 构建中，前端构建产物位于 app/static/admin
import os
from fastapi.responses import FileResponse

# 静态文件目录
static_dir = os.path.join(os.path.dirname(__file__), "static")
admin_dist_dir = os.path.join(static_dir, "admin")

# 如果存在构建的前端文件，挂载它
if os.path.exists(admin_dist_dir):
    # 挂载静态资源 (assets, etc.)
    app.mount("/assets", StaticFiles(directory=os.path.join(admin_dist_dir, "assets")), name="assets")
    
    # 挂载其他可能的静态文件根目录 (如 favicon.ico)
    # 注意：这可能会覆盖 API 路由，所以要小心。
    # 更好的方式是只挂载 assets，并用 catch-all 路由服务 index.html

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


# 注册 API 路由 (API 路由必须在 SPA catch-all 之前注册，如果 SPA catch-all 是通配符)
# 但上面的 SPA catch-all 定义使用了 app.get("/{full_path:path}")，这会匹配所有 GET 请求。
# 所以我们应该先注册 API 路由，然后再定义 SPA catch-all。

from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.app.api_v1_prefix)

# SPA Catch-all (放在最后)
if os.path.exists(admin_dist_dir):
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # 检查文件是否存在
        file_path = os.path.join(admin_dist_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        # 默认返回 index.html
        return FileResponse(os.path.join(admin_dist_dir, "index.html"))
    
    # 根路径
    @app.get("/")
    async def root():
        return FileResponse(os.path.join(admin_dist_dir, "index.html"))
else:
    # 开发模式或未构建前端时
    @app.get("/")
    async def root():
        return {
            "message": f"欢迎使用{settings.app.name}",
            "version": settings.app.version,
            "docs": "/docs",
            "api": settings.app.api_v1_prefix,
            "note": "管理后台未构建，请运行 'npm run build' 或使用 Docker 部署"
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.app.debug,
        log_level=settings.logging.level.lower(),
    )
