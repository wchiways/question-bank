"""Mock AI服务提供商 - 用于测试"""
from app.providers.base import BaseAIProvider
from app.core.logger import get_logger

logger = get_logger(__name__)


class MockAIProvider(BaseAIProvider):
    """
    Mock AI提供商 - 用于测试

    Args:
        mock_response: 模拟的响应内容
    """

    def __init__(self, mock_response: str = "这是模拟的AI答案"):
        self.mock_response = mock_response
        logger.warning("🧪 使用Mock AI提供商（仅用于测试）")

    async def call(self, prompt: str) -> str:
        """
        模拟AI调用

        Args:
            prompt: 提示词（忽略）

        Returns:
            模拟的响应
        """
        logger.info(f"🧪 Mock AI调用: {prompt[:50]}...")
        return f'{{"answer": "{self.mock_response}"}}'

    def get_model_name(self) -> str:
        """
        获取模型名称

        Returns:
            mock-model
        """
        return "mock-model"
