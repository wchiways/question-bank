"""AI 服务商配置管理 API"""
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.core.config import config_manager
from app.api import deps

router = APIRouter()


def mask_api_key(api_key: str) -> str:
    """
    脱敏处理 API Key

    Args:
        api_key: 原始 API Key

    Returns:
        脱敏后的 API Key (sk-****...****)
    """
    if not api_key or api_key.startswith("YOUR_"):
        return "未配置"

    if len(api_key) <= 8:
        return "****"

    return f"{api_key[:4]}{'*' * 8}{api_key[-4:]}"


@router.get("/providers")
async def get_providers():
    """
    获取所有AI服务商配置（API Key已脱敏）

    Returns:
        包含所有服务商配置的字典
    """
    config = config_manager.config.ai
    providers = {}

    for key, provider in config.providers.items():
        providers[key] = {
            "name": provider.name,
            "enabled": provider.enabled,
            "api_key": mask_api_key(provider.api_key),
            "api_url": provider.api_url,
            "model": provider.model,
            "max_tokens": provider.max_tokens,
            "temperature": provider.temperature,
        }

    return {
        "default_provider": config.default_provider,
        "timeout": config.timeout,
        "max_retries": config.max_retries,
        "providers": providers
    }


@router.put("/providers/{provider_key}")
async def update_provider(
    provider_key: str,
    config_data: Dict[str, Any] = Body(...)
):
    """
    更新指定服务商配置

    Args:
        provider_key: 服务商标识符 (如 openai, volcengine)
        config_data: 要更新的配置数据

    Returns:
        更新结果消息
    """
    ai_config = config_manager.config.ai

    if provider_key not in ai_config.providers:
        raise HTTPException(
            status_code=404,
            detail=f"服务商 '{provider_key}' 不存在"
        )

    # 更新配置
    provider = ai_config.providers[provider_key]
    for key, value in config_data.items():
        if hasattr(provider, key):
            # 如果是脱敏的 API Key，则跳过更新
            if key == "api_key" and value.startswith("****"):
                continue
            setattr(provider, key, value)

    config_manager.save()
    return {"message": f"服务商 '{provider_key}' 配置更新成功"}


@router.post("/providers/{provider_key}/test")
async def test_provider(provider_key: str):
    """
    测试服务商连接

    Args:
        provider_key: 服务商标识符

    Returns:
        测试结果，包含延迟、模型、使用量等信息
    """
    from app.services.ai_service import AIServiceTester

    try:
        result = await AIServiceTester.test_provider(provider_key)
        return {
            "success": True,
            "provider": provider_key,
            "latency": result["latency"],
            "model": result.get("model", "unknown"),
            "usage": result.get("usage", {}),
            "response": result.get("response", "")
        }
    except Exception as e:
        return {
            "success": False,
            "provider": provider_key,
            "error": str(e)
        }


@router.put("/default-provider")
async def set_default_provider(
    provider_key: str = Body(..., embed=True)
):
    """
    设置默认服务商

    Args:
        provider_key: 要设置为默认的服务商标识符

    Returns:
        设置结果消息
    """
    ai_config = config_manager.config.ai

    if provider_key not in ai_config.providers:
        raise HTTPException(
            status_code=404,
            detail=f"服务商 '{provider_key}' 不存在"
        )

    if not ai_config.providers[provider_key].enabled:
        raise HTTPException(
            status_code=400,
            detail=f"服务商 '{provider_key}' 未启用，无法设为默认"
        )

    ai_config.default_provider = provider_key
    config_manager.save()

    return {
        "message": f"已将 '{ai_config.providers[provider_key].name}' 设为默认服务商",
        "provider": provider_key
    }


@router.post("/providers/batch-enable")
async def batch_enable_providers(
    provider_keys: list[str] = Body(..., embed=True)
):
    """
    批量启用服务商

    Args:
        provider_keys: 要启用的服务商标识符列表

    Returns:
        批量操作结果
    """
    ai_config = config_manager.config.ai
    results = []

    for key in provider_keys:
        if key in ai_config.providers:
            ai_config.providers[key].enabled = True
            results.append({"provider": key, "success": True})
        else:
            results.append({"provider": key, "success": False, "error": "不存在"})

    config_manager.save()

    return {
        "message": f"批量启用完成，成功 {sum(r['success'] for r in results)}/{len(results)} 个",
        "results": results
    }


@router.post("/providers/batch-disable")
async def batch_disable_providers(
    provider_keys: list[str] = Body(..., embed=True)
):
    """
    批量禁用服务商

    Args:
        provider_keys: 要禁用的服务商标识符列表

    Returns:
        批量操作结果
    """
    ai_config = config_manager.config.ai
    default_provider = ai_config.default_provider
    results = []

    for key in provider_keys:
        if key in ai_config.providers:
            # 如果要禁用默认提供商，需要先更换默认提供商
            if key == default_provider:
                # 找第一个已启用的提供商作为新的默认提供商
                new_default = None
                for pk, pv in ai_config.providers.items():
                    if pv.enabled and pk != key:
                        new_default = pk
                        break

                if new_default:
                    ai_config.default_provider = new_default
                else:
                    results.append({
                        "provider": key,
                        "success": False,
                        "error": "无法禁用唯一的已启用提供商"
                    })
                    continue

            ai_config.providers[key].enabled = False
            results.append({"provider": key, "success": True})
        else:
            results.append({"provider": key, "success": False, "error": "不存在"})

    config_manager.save()

    return {
        "message": f"批量禁用完成，成功 {sum(r['success'] for r in results)}/{len(results)} 个",
        "results": results
    }


@router.post("/providers")
async def create_provider(
    provider_data: Dict[str, Any] = Body(...)
):
    """
    创建新的AI服务商

    Args:
        provider_data: 服务商配置数据，必须包含 key, name, api_key, api_url, model

    Returns:
        创建结果消息
    """
    from app.core.config import AIProviderConfig

    ai_config = config_manager.config.ai

    # 验证必填字段
    required_fields = ["key", "name", "api_key", "api_url", "model"]
    missing_fields = [f for f in required_fields if f not in provider_data or not provider_data[f]]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"缺少必填字段: {', '.join(missing_fields)}"
        )

    provider_key = provider_data["key"]

    # 检查key是否已存在
    if provider_key in ai_config.providers:
        raise HTTPException(
            status_code=400,
            detail=f"服务商标识符 '{provider_key}' 已存在"
        )

    # 创建新服务商配置
    try:
        new_provider = AIProviderConfig(
            name=provider_data["name"],
            api_key=provider_data["api_key"],
            api_url=provider_data["api_url"],
            model=provider_data["model"],
            enabled=provider_data.get("enabled", True),
            max_tokens=provider_data.get("max_tokens", 512),
            temperature=provider_data.get("temperature", 0.1)
        )

        ai_config.providers[provider_key] = new_provider
        config_manager.save()

        return {
            "message": f"服务商 '{new_provider.name}' 创建成功",
            "provider_key": provider_key
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"创建服务商失败: {str(e)}"
        )


@router.delete("/providers/{provider_key}")
async def delete_provider(provider_key: str):
    """
    删除指定的AI服务商

    Args:
        provider_key: 服务商标识符

    Returns:
        删除结果消息
    """
    ai_config = config_manager.config.ai

    if provider_key not in ai_config.providers:
        raise HTTPException(
            status_code=404,
            detail=f"服务商 '{provider_key}' 不存在"
        )

    # 如果要删除的是默认提供商，需要先更换默认提供商
    if provider_key == ai_config.default_provider:
        # 找第一个已启用的提供商作为新的默认提供商
        new_default = None
        for pk, pv in ai_config.providers.items():
            if pv.enabled and pk != provider_key:
                new_default = pk
                break

        if new_default:
            ai_config.default_provider = new_default
        else:
            raise HTTPException(
                status_code=400,
                detail="无法删除唯一的提供商，请先添加其他提供商"
            )

    provider_name = ai_config.providers[provider_key].name
    del ai_config.providers[provider_key]
    config_manager.save()

    return {
        "message": f"服务商 '{provider_name}' 已删除",
        "provider_key": provider_key
    }
