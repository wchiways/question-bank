"""工具函数 - 辅助功能"""
import re
from typing import Optional
from app.core.logger import get_logger

logger = get_logger(__name__)


def match_option(answer: str, options: str) -> str:
    """
    智能匹配答案到选项

    如果答案不包含字母前缀（如"A."），尝试从选项中匹配
    
    Args:
        answer: AI返回的答案
        options: 选项字符串
        
    Returns:
        匹配后的完整选项（如"A. xxx"）
    """
    # 如果答案已经包含字母前缀，直接返回
    if re.match(r'^[A-Z][.、]\s', answer):
        return answer
    
    # 解析选项列表
    option_list = []
    raw_options = []
    for part in options.split():
        # 保存原始选项用于后备匹配
        raw_options.append(part)
        
        # 匹配 "A. xxx" 或 "A．xxx" 或 "A xxx" 格式
        match = re.match(r'^([A-Z])[.、、\s]+(.+)$', part)
        if match:
            letter = match.group(1)
            content = match.group(2)
            option_list.append({
                'letter': letter,
                'full': f"{letter}. {content}",
                'content': content
            })
    
    # 1. 尝试结构化选项精确匹配
    for option in option_list:
        if answer == option['content']:
            logger.info(f"✅ 精确匹配: '{answer}' -> '{option['full']}'")
            return option['full']
    
    # 2. 尝试结构化选项包含匹配
    for option in option_list:
        if option['content'] in answer or answer in option['content']:
            logger.info(f"✅ 包含匹配: '{answer}' -> '{option['full']}'")
            return option['full']
            
    # 3. 如果没有结构化选项或匹配失败，尝试原始选项匹配 (针对判断题/简单选项)
    if answer in raw_options:
        logger.info(f"✅ 原始选项匹配: '{answer}'")
        return answer
    
    # 如果都匹配不上，返回原答案
    logger.warning(f"⚠️ 无法匹配答案: {answer} (选项: {options})")
    return answer


def extract_first_answer(answer: str) -> str:
    """
    从多答案中提取第一个答案
    
    Args:
        answer: 答案字符串（可能包含###）
        
    Returns:
        第一个答案
    """
    if '###' in answer:
        return answer.split('###')[0]
    return answer
