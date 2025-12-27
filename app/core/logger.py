"""日志系统配置 - 使用loguru进行结构化日志管理"""
import sys
import logging
from pathlib import Path
from loguru import logger as loguru_logger
from app.core.config import settings


class InterceptHandler(logging.Handler):
    """将标准logging重定向到loguru"""

    def emit(self, record):
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger():
    """配置loguru日志系统"""
    import logging

    # 移除默认handler
    loguru_logger.remove()

    # 控制台输出 - 彩色格式
    loguru_logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # 文件输出 - JSON格式
    log_path = Path(settings.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    loguru_logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation=settings.LOG_ROTATION,
        retention="30 days",
        compression="zip",
    )

    # 拦截标准logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)


def get_logger(name: str):
    """
    获取logger实例

    Args:
        name: logger名称，通常使用__name__

    Returns:
        绑定名称的logger实例
    """
    return loguru_logger.bind(name=name)


# 应用启动时配置日志
setup_logger()
