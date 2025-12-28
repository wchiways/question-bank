"""通用AI服务提供商 - 支持多个AI平台"""
import asyncio
import json
from typing import Optional
import httpx
from app.providers.base import BaseAIProvider
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class UniversalAIProvider(BaseAIProvider):
    """
    通用AI服务提供商 - 支持OpenAI兼容的API

    支持的平台:
    - SiliconFlow (硅基流动)
    - Ali Bailian (阿里百炼)
    - Zhipu AI (智谱AI)
    - Volcengine (火山引擎)
    - OpenAI
    - 其他兼容OpenAI API格式的平台
    """

    def __init__(self, provider_name: str):
        """
        初始化通用AI提供商

        Args:
            provider_name: 提供商名称 (siliconflow/ali_bailian/zhipu/openai/google)
        """
        self.provider_name = provider_name

        # 从配置中获取提供商配置
        provider_config = settings.ai.providers.get(provider_name)
        if not provider_config:
            raise ValueError(f"❌ 未找到AI提供商配置: {provider_name}")

        self.config = provider_config
        self.api_key = provider_config.api_key
        self.model = provider_config.model
        self.api_url = provider_config.api_url
        self.timeout = settings.ai.timeout
        self.max_retries = settings.ai.max_retries
        self.max_tokens = provider_config.max_tokens
        self.temperature = provider_config.temperature

        if not self.config.enabled:
            logger.warning(f"⚠️  AI提供商 {provider_name} 未启用")
        else:
            logger.info(f"✅ 初始化AI提供商: {self.config.name} ({self.model})")

    async def call(self, prompt: str) -> str:
        """
        异步调用AI服务

        Args:
            prompt: 提示词

        Returns:
            AI返回的文本
        """
        if not self.config.enabled:
            logger.error(f"❌ AI提供商 {self.provider_name} 未启用")
            return ""

        if not self.api_key or self.api_key == "" or self.api_key.startswith("YOUR_"):
            logger.error(f"❌ {self.provider_name} API密钥未配置")
            return ""

        # Google Gemini使用不同的API格式
        if self.provider_name == "google":
            return await self._call_google(prompt)

        # OpenAI兼容格式 (SiliconFlow, Ali Bailian, Zhipu, OpenAI等)
        return await self._call_openai_compatible(prompt)

    async def _call_openai_compatible(self, prompt: str) -> str:
        """
        调用OpenAI兼容格式的API

        Args:
            prompt: 提示词

        Returns:
            AI返回的文本
        """
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 阿里百炼需要特殊的Header
        if self.provider_name == "ali_bailian":
            headers["Authorization"] = f"Bearer {self.api_key}"

        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.info(f"📤 调用 {self.config.name} (尝试 {retry_count + 1}/{self.max_retries})")
                    response = await client.post(self.api_url, json=payload, headers=headers)
                    response.raise_for_status()

                    result = response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        answer = result["choices"][0]["message"]["content"]
                        logger.info(f"✅ {self.config.name} 调用成功")
                        return answer
                    else:
                        logger.error(f"❌ API响应格式异常: {result}")
                        return ""

            except httpx.TimeoutException:
                last_error = "API请求超时"
                logger.warning(f"⏱️  {last_error}")
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

        logger.error(f"❌ {self.config.name} 调用失败，已达最大重试次数")
        return ""

    async def _call_google(self, prompt: str) -> str:
        """
        调用Google Gemini API

        Args:
            prompt: 提示词

        Returns:
            AI返回的文本
        """
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": self.temperature,
                "maxOutputTokens": self.max_tokens
            }
        }

        # Google API URL需要包含API Key
        api_url_with_key = f"{self.api_url}?key={self.api_key}"

        retry_count = 0
        last_error = None

        while retry_count < self.max_retries:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    logger.info(f"📤 调用 {self.config.name} (尝试 {retry_count + 1}/{self.max_retries})")
                    response = await client.post(
                        api_url_with_key,
                        json=payload,
                        headers={"Content-Type": "application/json"}
                    )
                    response.raise_for_status()

                    result = response.json()
                    if "candidates" in result and len(result["candidates"]) > 0:
                        answer = result["candidates"][0]["content"]["parts"][0]["text"]
                        logger.info(f"✅ {self.config.name} 调用成功")
                        return answer
                    else:
                        logger.error(f"❌ API响应格式异常: {result}")
                        return ""

            except httpx.TimeoutException:
                last_error = "API请求超时"
                logger.warning(f"⏱️  {last_error}")
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP错误: {e.response.status_code}"
                logger.warning(f"❌ {last_error}")
            except Exception as e:
                last_error = str(e)
                logger.error(f"❌ API调用失败: {e}")

            retry_count += 1
            if retry_count < self.max_retries:
                wait_time = min(2 ** retry_count, 10)
                logger.info(f"⏳ {wait_time}秒后重试...")
                await asyncio.sleep(wait_time)

        logger.error(f"❌ {self.config.name} 调用失败，已达最大重试次数")
        return ""

    def get_model_name(self) -> str:
        """
        获取模型名称

        Returns:
            模型名称
        """
        return self.model
