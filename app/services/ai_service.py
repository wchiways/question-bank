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
            "single": "单选题：只返回一个正确选项的完整内容，不要包含字母前缀（如A. B. C.），直接返回选项文字。",
            "multiple": "多选题：如果有多个正确答案，用三个井号###连接每个答案的内容。",
            "judgement": "判断题：直接返回'对'或'错'。",
            "fill": "填空题：直接返回填空内容，如果有多个空，用###连接。"
        }
        
        instruction = type_instructions.get(question_type, type_instructions["single"])
        
        base_prompt = f'''你是一个专业的题库系统，请根据问题提供准确的答案。

{instruction}

重要：
- 只返回答案内容，不要包含任何解释或额外文字
- 不要返回字母编号（如A、B、C）
- 严格使用JSON格式：{{"answer":"答案内容"}}
- 不要返回任何自然语言描述

例如：
- 如果答案是"A. 北京"，只返回"北京"
- 如果答案是"对"或"错"，直接返回"对"或"错"
- 如果填空题答案是"北京###上海"，返回"北京###上海"

问题：{title}'''

        if options:
            base_prompt += f'\n选项：{options}'

        return base_prompt

    def _parse_response(self, response: str) -> Optional[str]:
        """
        解析AI响应

        Args:
            response: AI返回的原始文本

        Returns:
            提取的答案或None
        """
        if not response:
            return None

        try:
            # 尝试提取JSON部分
            if "{" in response and "}" in response:
                start_idx = response.find("{")
                end_idx = response.rfind("}") + 1
                json_str = response[start_idx:end_idx]

                # 清理JSON字符串
                json_str = json_str.replace("'", '"')
                json_str = re.sub(r'{\s*(\w+)(\s*:)', r'{"\1"\2', json_str)
                json_str = re.sub(r',\s*(\w+)(\s*:)', r',"\1"\2', json_str)
                json_str = re.sub(r'\s+', ' ', json_str).strip()

                # 解析JSON
                data = json.loads(json_str)

                # 提取answer（兼容拼写错误）
                if "answer" in data:
                    return data["answer"]
                elif "anwser" in data:
                    return data["anwser"]

            # 如果JSON解析失败，尝试正则提取
            answer_match = re.search(r'"answer"\s*:\s*"([^"]+)"', response)
            if answer_match:
                return answer_match.group(1)

            return None

        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON解析失败: {e}, 原始响应: {response[:200]}")
            return None
        except Exception as e:
            logger.error(f"❌ 解析响应失败: {e}")
            return None
