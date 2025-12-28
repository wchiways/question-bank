"""AI异步服务 - 封装AI调用逻辑和响应解析"""
import json
import re
import time
from typing import Optional
from app.core.config import settings
from app.core.logger import get_logger
from app.providers.multi_provider import UniversalAIProvider
from app.providers.mock_provider import MockAIProvider
from app.repositories.stats_repository import StatsRepository
from app.repositories.log_repository import LogRepository

logger = get_logger(__name__)


class AIAsyncService:
    """
    AI异步服务 - 封装AI调用逻辑，支持多个AI服务商
    """

    def __init__(
        self,
        stats_repo: Optional[StatsRepository] = None,
        log_repo: Optional[LogRepository] = None,
        provider_name: Optional[str] = None
    ):
        """
        初始化AI服务

        Args:
            stats_repo: 统计仓储
            log_repo: 日志仓储
            provider_name: 指定的提供商名称，如果不指定则使用配置中的默认提供商
        """
        self.stats_repo = stats_repo
        self.log_repo = log_repo
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

            start_time = time.time()
            error_msg = None
            response = ""
            
            try:
                # 调用AI
                response = await self.provider.call(prompt)
            except Exception as e:
                error_msg = str(e)
                raise e
            finally:
                end_time = time.time()
                latency = int((end_time - start_time) * 1000)
                
                # 记录详细日志
                if self.log_repo:
                    try:
                        await self.log_repo.create_log(
                            provider=self.provider_name,
                            model=self.provider.get_model_name() if hasattr(self.provider, 'get_model_name') else "unknown",
                            prompt_length=len(prompt),
                            response_length=len(response) if response else 0,
                            latency_ms=latency,
                            success=error_msg is None,
                            error_message=error_msg
                        )
                    except Exception as e:
                        logger.error(f"❌ 记录详细日志失败: {e}")

            # 记录统计
            if self.stats_repo and not error_msg:
                try:
                    await self.stats_repo.increment_call_count(self.provider_name)
                except Exception as e:
                    logger.error(f"❌ 记录统计失败: {e}")

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
