"""应用配置管理 - 从config.json读取配置"""
import json
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AIProviderConfig(BaseModel):
    """AI服务提供商配置"""
    name: str
    enabled: bool = True
    api_key: str
    api_url: str
    model: str
    max_tokens: int = 512
    temperature: float = 0.1


class AIConfig(BaseModel):
    """AI配置"""
    default_provider: str = "siliconflow"
    timeout: int = 30
    max_retries: int = 3
    providers: Dict[str, AIProviderConfig] = {}


class AppConfig(BaseModel):
    """应用配置"""
    name: str = "OCS题库系统"
    version: str = "2.0.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"


class ServerConfig(BaseModel):
    """服务器配置"""
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseConfig(BaseModel):
    """数据库配置"""
    url: str = "sqlite+aiosqlite:///./question_bank.db"
    echo: bool = False


class CacheConfig(BaseModel):
    """缓存配置"""
    type: str = "memory"
    ttl: int = 3600
    redis_url: Optional[str] = None


class RateLimitConfig(BaseModel):
    """限流配置"""
    enabled: bool = True
    per_minute: int = 60


class LoggingConfig(BaseModel):
    """日志配置"""
    level: str = "INFO"
    file: str = "logs/app.log"
    rotation: str = "10 MB"


class SecurityConfig(BaseModel):
    """安全配置"""
    secret_key: str
    allowed_hosts: list[str] = ["*"]


class Settings(BaseModel):
    """应用总配置"""
    app: AppConfig = Field(default_factory=AppConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    rate_limit: RateLimitConfig = Field(default_factory=RateLimitConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)

    class Config:
        validate_assignment = True


def load_config(config_path: str = "config.json") -> Settings:
    """
    从JSON文件加载配置

    Args:
        config_path: 配置文件路径

    Returns:
        Settings对象
    """
    config_file = Path(config_path)

    # 如果配置文件不存在，创建默认配置
    if not config_file.exists():
        print(f"⚠️  配置文件 {config_path} 不存在，使用默认配置")
        return Settings()

    with open(config_file, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    return Settings(**config_data)


# 全局配置实例
settings = load_config()

# 便捷属性访问
APP_NAME = settings.app.name
APP_VERSION = settings.app.version
DEBUG = settings.app.debug
API_V1_PREFIX = settings.app.api_v1_prefix

HOST = settings.server.host
PORT = settings.server.port

DATABASE_URL = settings.database.url
DATABASE_ECHO = settings.database.echo

AI_PROVIDER = settings.ai.default_provider
AI_TIMEOUT = settings.ai.timeout
AI_MAX_RETRIES = settings.ai.max_retries

CACHE_TYPE = settings.cache.type
CACHE_TTL = settings.cache.ttl

RATE_LIMIT_ENABLED = settings.rate_limit.enabled
RATE_LIMIT_PER_MINUTE = settings.rate_limit.per_minute

LOG_LEVEL = settings.logging.level
LOG_FILE = settings.logging.file
LOG_ROTATION = settings.logging.rotation

SECRET_KEY = settings.security.secret_key
ALLOWED_HOSTS = settings.security.allowed_hosts
