"""AI服务提供商基类 - 定义AI服务接口"""
from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """AI服务提供商基类"""

    @abstractmethod
    async def call(self, prompt: str) -> str:
        """
        调用AI服务

        Args:
            prompt: 提示词

        Returns:
            AI返回的文本
        """
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """
        获取模型名称

        Returns:
            模型名称
        """
        pass
