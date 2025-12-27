"""应用配置管理 - 使用Pydantic Settings进行类型安全的配置管理"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """应用配置 - 类型安全的环境变量管理"""

    # 应用基础配置
    APP_NAME: str = "OCS题库系统"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./question_bank.db"
    DATABASE_ECHO: bool = False

    # AI服务配置
    AI_PROVIDER: str = "siliconflow"  # siliconflow, openai, mock
    AI_MODEL: str = "Qwen/QwQ-32B"
    AI_API_KEY: str
    AI_API_URL: str = "https://api.siliconflow.cn/v1/chat/completions"
    AI_TIMEOUT: int = 30
    AI_MAX_RETRIES: int = 3

    # 缓存配置
    CACHE_TYPE: str = "memory"  # memory, redis
    CACHE_TTL: int = 3600  # 1小时
    REDIS_URL: Optional[str] = None

    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_ROTATION: str = "10 MB"

    # 安全配置
    SECRET_KEY: str
    ALLOWED_HOSTS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# 全局配置实例
settings = Settings()
