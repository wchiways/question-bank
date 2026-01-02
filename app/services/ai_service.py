"""AI异步服务 - 封装AI调用逻辑和响应解析"""
import json
import re
from typing import Optional
from app.core.config import settings
from app.core.logger import get_logger
from app.providers.multi_provider import UniversalAIProvider
from app.providers.mock_provider import MockAIProvider

logger = get_logger(__name__)


class AIAsyncService:
    """
    AI异步服务 - 封装AI调用逻辑，支持多个AI服务商
    """

    def __init__(self, provider_name: Optional[str] = None):
        """
        初始化AI服务

        Args:
            provider_name: 指定的提供商名称，如果不指定则使用配置中的默认提供商
        """
        self.provider_name = provider_name or settings.ai.default_provider

        # 获取提供商配置
        provider_config = settings.ai.providers.get(self.provider_name)

        # 如果提供商未配置或未启用，使用Mock
        if not provider_config or not provider_config.enabled:
            logger.warning(f"⚠️  AI提供商 {self.provider_name} 未配置或未启用，使用Mock提供商")
            self.provider = MockAIProvider()
        else:
            try:
                self.provider = UniversalAIProvider(self.provider_name)
                logger.info(f"✅ AI服务已初始化: {provider_config.name}")
            except Exception as e:
                logger.error(f"❌ 初始化AI提供商失败: {e}")
                self.provider = MockAIProvider()

    async def get_answer(
        self,
        title: str,
        options: str = "",
        question_type: str = ""
    ) -> Optional[str]:
        """
        获取AI答案

        Args:
            title: 问题标题
            options: 选项
            question_type: 题目类型

        Returns:
            答案文本或None
        """
        try:
            # 构建提示词
            prompt = self._build_prompt(title, options, question_type)

            # 调用AI
            response = await self.provider.call(prompt)

            # 解析响应
            answer = self._parse_response(response)

            if answer:
                logger.info(f"✅ AI返回答案: {title[:50]}... -> {answer[:50]}...")
            else:
                logger.warning(f"⚠️ AI未返回有效答案: {title[:50]}...")

            return answer

        except Exception as e:
            logger.error(f"❌ AI服务调用失败: {e}")
            return None

    def _build_prompt(
        self,
        title: str,
        options: str,
        question_type: str
    ) -> str:
        """
        构建AI提示词

        Args:
            title: 问题标题
            options: 选项
            question_type: 题目类型

        Returns:
            完整的提示词
        """
        # 根据题目类型提供更详细的说明
        type_instructions = {
            "single": "单选题：返回完整答案，包括字母和内容，例如：'A. 答案内容' 或 'A'。",
            "multiple": "多选题：如果有多个正确答案，用###连接每个完整答案，包括字母，例如：'A. 答案一###C. 答案二'。",
            "judgement": "判断题：直接返回'对'或'错'。",
            "fill": "填空题：直接返回填空内容，如果有多个空，用###连接。"
        }
        
        instruction = type_instructions.get(question_type, type_instructions["single"])
        
        # 如果有选项，添加示例说明
        options_help = ""
        if options:
            options_help = f"""
重要：必须返回完整答案格式！
- 如果答案是A选项，必须返回"A. 选项内容"
- 不能只返回"选项内容"或"A"
- 必须包含字母和完整文字

示例：
问题：Access数据库的特点是？
选项：A. 关系模型 B. 层次模型 C. 网状模型 D. 面向对象模型
正确答案：A. 关系模型  （而不是只返回"关系模型"）
"""
        
        base_prompt = f'''你是一个专业的题库系统，请根据问题提供准确的答案。

{instruction}
{options_help}

问题：{title}'''

        if options:
            base_prompt += f'\n选项：{options}'

        return base_prompt

    def _parse_response(self, response: str) -> Optional[str]:
        """
        解析AI响应 - 智能提取答案，支持多种格式

        Args:
            response: AI返回的原始文本

        Returns:
            提取的答案或None
        """
        if not response:
            return None

        try:
            # 清理响应
            response = response.strip()
            
            # 方法1: 尝试提取JSON格式的answer
            json_match = re.search(r'"answer"\s*:\s*"([^"]+)"', response, re.IGNORECASE)
            if json_match:
                answer = json_match.group(1)
                logger.info(f"✅ JSON格式解析成功: {answer[:50]}...")
                return self._format_answer(answer, response)
            
            # 方法2: 如果有选项，尝试匹配选项
            # 从AI服务初始化时获取选项（这里简化处理）
            # 先尝试找到匹配的选项
            
            # 方法3: 直接返回清理后的文本
            # 移除常见的多余文字
            cleaned = re.sub(r'^(答案是?|结果为?|正确答案是?)[:：]*\s*', '', response)
            cleaned = cleaned.strip()
            
            if cleaned and len(cleaned) > 0:
                logger.info(f"✅ 直接使用清理后的答案: {cleaned[:50]}...")
                return cleaned
            
            logger.warning(f"⚠️ 无法解析AI响应: {response[:100]}")
            return None

        except Exception as e:
            logger.error(f"❌ 解析响应失败: {e}")
            return None
    
    def _format_answer(self, answer: str, full_response: str) -> str:
        """
        格式化答案，确保包含选项字母
        
        Args:
            answer: 提取的答案
            full_response: 完整响应
            
        Returns:
            格式化后的答案
        """
        # 如果答案已经是完整格式（A. xxx），直接返回
        if re.match(r'^[A-Z][.、]\s', answer):
            return answer
        
        # 如果只是答案内容（xxx），尝试从选项中匹配
        # 这里简化处理，直接返回原答案
        # 实际使用时，可以在API层根据选项进行匹配

        return answer


class AIServiceTester:
    """
    AI 服务商连接测试器
    用于测试各个 AI 服务商的连接和可用性
    """

    @staticmethod
    async def test_provider(provider_key: str) -> dict:
        """
        测试指定 AI 服务商的连接和可用性

        Args:
            provider_key: 服务商标识符 (如 openai, volcengine)

        Returns:
            包含测试结果的字典:
            - latency: 响应时间（毫秒）
            - model: 实际使用的模型名称
            - usage: token 使用情况
            - response: 测试响应内容

        Raises:
            Exception: 当服务商未启用或连接失败时
        """
        import time
        import httpx

        config = settings.ai.providers

        if provider_key not in config:
            raise Exception(f"服务商 '{provider_key}' 不存在")

        provider_config = config[provider_key]

        if not provider_config.enabled:
            raise Exception(f"服务商 '{provider_key}' 未启用")

        if not provider_config.api_key or provider_config.api_key.startswith("YOUR_"):
            raise Exception(f"服务商 '{provider_key}' API Key 未配置")

        logger.info(f"开始测试服务商: {provider_key}")

        start_time = time.time()

        try:
            async with httpx.AsyncClient(timeout=settings.ai.timeout) as client:
                # 构建测试请求
                payload = {
                    "model": provider_config.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Hi"
                        }
                    ],
                    "max_tokens": 10,
                    "temperature": provider_config.temperature
                }

                # 发送请求
                response = await client.post(
                    provider_config.api_url,
                    headers={
                        "Authorization": f"Bearer {provider_config.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

                latency = (time.time() - start_time) * 1000

                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"服务商 {provider_key} 测试成功，延迟: {latency:.2f}ms")

                    return {
                        "latency": int(latency),
                        "model": data.get("model", provider_config.model),
                        "usage": data.get("usage", {
                            "prompt_tokens": 0,
                            "completion_tokens": 0,
                            "total_tokens": 0
                        }),
                        "response": data.get("choices", [{}])[0].get("message", {}).get("content", "")
                    }
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    logger.error(f"服务商 {provider_key} 测试失败: {error_msg}")
                    raise Exception(error_msg)

        except httpx.TimeoutException:
            logger.error(f"服务商 {provider_key} 请求超时")
            raise Exception(f"连接超时（超过 {settings.ai.timeout} 秒）")

        except httpx.ConnectError as e:
            logger.error(f"服务商 {provider_key} 连接失败: {e}")
            raise Exception(f"网络连接失败: {str(e)}")

        except Exception as e:
            logger.error(f"服务商 {provider_key} 测试异常: {e}")
            raise

    @staticmethod
    async def get_provider_status(provider_key: str) -> dict:
        """
        获取服务商状态信息

        Args:
            provider_key: 服务商标识符

        Returns:
            包含状态信息的字典
        """
        config = settings.ai.providers

        if provider_key not in config:
            return {
                "exists": False,
                "enabled": False,
                "configured": False
            }

        provider_config = config[provider_key]

        return {
            "exists": True,
            "enabled": provider_config.enabled,
            "configured": bool(
                provider_config.api_key and
                not provider_config.api_key.startswith("YOUR_")
            ),
            "name": provider_config.name,
            "model": provider_config.model
        }
