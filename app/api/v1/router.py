"""API路由聚合 - v1版本所有路由"""
from fastapi import APIRouter
from app.api.v1.endpoints import query, health

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(query.router, tags=["查询"])
api_router.include_router(health.router, tags=["系统"])
