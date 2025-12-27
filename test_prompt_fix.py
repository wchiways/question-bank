import asyncio
from app.services.ai_service import AIAsyncService

async def test():
    service = AIAsyncService()
    
    # 测试单选题
    print("=== 测试单选题 ===")
    result = await service.get_answer(
        "算法的特征是",
        "A. 有穷性 B. 确定性 C. 输入输出 D. 可行性或能行性",
        "single"
    )
    print(f"答案: {result}")
    print()

asyncio.run(test())
