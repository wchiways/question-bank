from fastapi import APIRouter, HTTPException, Body
from app.core.config import config_manager, Settings
from typing import Any, Dict

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def get_config():
    """获取当前系统配置"""
    # 转换为字典并排除敏感信息（如 API Key）
    config_dict = config_manager.config.model_dump()
    # 注意：在生产环境中应该更严格地过滤 api_key
    return config_dict

@router.put("/")
async def update_config(new_config: Dict[str, Any] = Body(...)):
    """更新系统配置"""
    try:
        # 简单校验并更新
        # 在实际应用中，应该逐项校验
        for key, value in new_config.items():
            if hasattr(config_manager.config, key):
                setattr(config_manager.config, key, value)
        
        config_manager.save()
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/reload")
async def reload_config():
    """重新加载配置文件"""
    config_manager.reload()
    return {"message": "Configuration reloaded"}