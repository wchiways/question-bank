"""SiliconFlow AI服务提供商 - 使用httpx实现异步调用"""
import asyncio
import json
from typing import Optional
import httpx
from app.providers.base import BaseAIProvider
from app.core.logger import get_logger

logger = get_logger(__name__)


class SiliconFlowProvider(BaseAIProvider):
    """
    SiliconFlow AI服务提供商

    Args:
        api_key: API密钥
        model: 模型名称
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
    """

    def __init__(
        self,
        api_key: str,
        model: str = "Qwen/QwQ-32B",
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.api_url = "https://api.siliconflow.cn/v1/chat/completions"

    async def call(self, prompt: str) -> str:
        """
        异步调用SiliconFlow API

        Args:
            prompt: 提示词

        Returns:
            AI返回的文本
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.1
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.info(f"📤 调用AI服务 (尝试 {retry_count + 1}/{self.max_retries})")
                    response = await client.post(self.api_url, json=payload, headers=headers)
                    response.raise_for_status()

                    result = response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        answer = result["choices"][0]["message"]["content"]
                        logger.info("✅ AI服务调用成功")
                        return answer
                    else:
                        logger.error(f"❌ API响应格式异常: {result}")
                        return ""

            except httpx.TimeoutException:
                last_error = "API请求超时"
                logger.warning(f"⏱️ {last_error}")
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP错误: {e.response.status_code}"
                logger.warning(f"❌ {last_error}")
            except Exception as e:
                last_error = str(e)
                logger.error(f"❌ API调用失败: {e}")

            retry_count += 1
            if retry_count < self.max_retries:
                # 指数退避
                wait_time = min(2 ** retry_count, 10)
                logger.info(f"⏳ {wait_time}秒后重试...")
                await asyncio.sleep(wait_time)

        logger.error(f"❌ AI服务调用失败，已达最大重试次数")
        return ""

    def get_model_name(self) -> str:
        """
        获取模型名称

        Returns:
            模型名称
        """
        return self.model
