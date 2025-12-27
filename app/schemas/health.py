"""健康检查相关的Schema定义"""
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    健康检查响应

    Attributes:
        status: 健康状态
        app_name: 应用名称
        version: 应用版本
        environment: 运行环境
    """
    status: str
    app_name: str
    version: str
    environment: str
