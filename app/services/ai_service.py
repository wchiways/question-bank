"""AI异步服务 - 封装AI调用逻辑和响应解析"""
import json
import re
from typing import Optional
from app.core.config import settings
from app.core.logger import get_logger
from app.providers.siliconflow_provider import SiliconFlowProvider
from app.providers.mock_provider import MockAIProvider

logger = get_logger(__name__)


class AIAsyncService:
    """
    AI异步服务 - 封装AI调用逻辑
    """

    def __init__(self):
        """初始化AI服务"""
        if settings.AI_PROVIDER == "mock":
            self.provider = MockAIProvider()
        else:
            self.provider = SiliconFlowProvider(
                api_key=settings.AI_API_KEY,
                model=settings.AI_MODEL,
                timeout=settings.AI_TIMEOUT,
                max_retries=settings.AI_MAX_RETRIES
            )

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
        base_prompt = '''你是一个题库接口函数，请根据问题和选项提供答案。如果是选择题，直接返回对应选项的内容，注意是内容，不是对应字母；如果题目是多选题，将内容用"###"连接；如果选项内容是"对","错"，且只有两项，或者question_type是judgement，你直接返回"对"或"错"的文字，不要返回字母；如果是填空题，直接返回填空内容，多个空使用###连接。回答格式为：{"answer":"your_answer_str"}，严格使用此格式回答。下面是一个问题，请你用json格式回答我，绝对不要使用自然语言'''

        question_data = {
            "问题": title,
            "选项": options,
            "类型": question_type
        }

        return base_prompt + f"\n{json.dumps(question_data, ensure_ascii=False)}"

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
