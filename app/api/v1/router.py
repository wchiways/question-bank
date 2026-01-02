"""API路由聚合 - v1版本所有路由"""
from fastapi import APIRouter
from app.api.v1.endpoints import query, health
from app.api.v1.endpoints import admin

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(query.router, tags=["查询"])
api_router.include_router(health.router, tags=["系统"])

# 注册管理后台路由
api_router.include_router(admin.questions_router, prefix="/admin/questions", tags=["管理-题库"])
api_router.include_router(admin.logs_router, prefix="/admin/logs", tags=["管理-日志"])
api_router.include_router(admin.stats_router, prefix="/admin/stats", tags=["管理-统计"])
api_router.include_router(admin.config_router, prefix="/admin/config", tags=["管理-配置"])
api_router.include_router(admin.database_router, prefix="/admin/database", tags=["管理-数据库"])
api_router.include_router(admin.ai_providers_router, prefix="/admin/ai", tags=["管理-AI服务商"])
