from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from app.core.config import config_manager, settings, AIProviderConfig, AppConfig, RateLimitConfig
from app.api.deps import get_stats_repo, get_ai_service, get_log_repo, get_api_key_repo, verify_api_key
from app.repositories.stats_repository import StatsRepository
from app.repositories.log_repository import LogRepository
from app.repositories.api_key_repository import ApiKeyRepository
from app.services.ai_service import AIAsyncService
from app.models.stats import ProviderStats
from app.models.log import CallLog
from app.models.api_key import ApiKey

router = APIRouter()

# Schemas
class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    token_type: str = "bearer"

class ProviderResponse(BaseModel):
    default: str
    providers: Dict[str, AIProviderConfig]

class TestAIRequest(BaseModel):
    provider_name: str
    prompt: str
    model: Optional[str] = None

class SystemConfig(BaseModel):
    app: AppConfig
    rate_limit: RateLimitConfig

# Endpoints

@router.post("/login", response_model=LoginResponse)
async def login(
    creds: LoginRequest,
    repo: ApiKeyRepository = Depends(get_api_key_repo)
):
    """
    Admin login endpoint
    Validates username and password against configured admin credentials
    """
    # Check against configured admin credentials
    if (creds.username == settings.security.admin_username and
        creds.password == settings.security.admin_password):
        # Return a special token that can be validated
        # In production, you should generate a proper JWT token
        return LoginResponse(
            access_token=f"admin-{creds.username}",
            token_type="bearer"
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/keys", response_model=List[ApiKey], dependencies=[Depends(verify_api_key)])
async def get_keys(repo: ApiKeyRepository = Depends(get_api_key_repo)):
    """Get all API keys"""
    return await repo.get_all_keys()

@router.post("/keys", response_model=ApiKey, dependencies=[Depends(verify_api_key)])
async def create_key(
    key: str = Body(..., embed=True),
    name: str = Body("Default", embed=True),
    repo: ApiKeyRepository = Depends(get_api_key_repo)
):
    """Create a new API key"""
    existing = await repo.find_by_key(key)
    if existing:
        raise HTTPException(status_code=400, detail="Key already exists")
    return await repo.create_key(key, name)

@router.delete("/keys/{key}", dependencies=[Depends(verify_api_key)])
async def delete_key(key: str, repo: ApiKeyRepository = Depends(get_api_key_repo)):
    """Delete an API key"""
    success = await repo.delete_by_key(key)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": "Key deleted"}

@router.get("/config", response_model=SystemConfig, dependencies=[Depends(verify_api_key)])
async def get_config():
    """Get system configuration"""
    return SystemConfig(
        app=settings.app,
        rate_limit=settings.rate_limit
    )

@router.post("/playground/test", dependencies=[Depends(verify_api_key)])
async def test_provider(
    request: TestAIRequest,
    ai_service: AIAsyncService = Depends(get_ai_service)
):
    """Test an AI provider"""
    try:
        service = AIAsyncService(provider_name=request.provider_name)
        if hasattr(service, 'provider'):
             response = await service.provider.call(request.prompt)
             return {"response": response}
        return {"error": "Could not access provider instance"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers", response_model=ProviderResponse, dependencies=[Depends(verify_api_key)])
async def get_providers():
    """Get all configured providers"""
    return {
        "default": settings.ai.default_provider,
        "providers": settings.ai.providers
    }

@router.post("/providers", dependencies=[Depends(verify_api_key)])
async def add_provider(name: str = Body(..., embed=True), config: AIProviderConfig = Body(...)):
    """Add or update a provider"""
    settings.ai.providers[name] = config
    config_manager.save()
    return {"message": "Provider saved", "provider": config}

@router.delete("/providers/{name}", dependencies=[Depends(verify_api_key)])
async def delete_provider(name: str):
    """Delete a provider"""
    if name not in settings.ai.providers:
        raise HTTPException(status_code=404, detail="Provider not found")
    del settings.ai.providers[name]
    config_manager.save()
    return {"message": "Provider deleted"}

@router.post("/providers/default", dependencies=[Depends(verify_api_key)])
async def set_default_provider(name: str = Body(..., embed=True)):
    """Set the default provider"""
    if name not in settings.ai.providers:
         raise HTTPException(status_code=404, detail="Provider not found")
    settings.ai.default_provider = name
    config_manager.save()
    return {"message": f"Default provider set to {name}"}

@router.get("/logs", response_model=List[CallLog], dependencies=[Depends(verify_api_key)])
async def get_logs(
    skip: int = 0,
    limit: int = 20,
    log_repo: LogRepository = Depends(get_log_repo)
):
    """Get paginated call logs"""
    return await log_repo.get_logs(skip=skip, limit=limit)

@router.get("/analysis/trend", dependencies=[Depends(verify_api_key)])
async def get_trend_analysis(
    days: int = 7,
    log_repo: LogRepository = Depends(get_log_repo)
):
    """Get call trend analysis"""
    stats = await log_repo.get_daily_stats(days=days)
    return [
        {
            "date": str(s.date),
            "count": s.count,
            "avg_latency": round(s.avg_latency, 2)
        }
        for s in stats
    ]

@router.get("/stats", response_model=List[ProviderStats], dependencies=[Depends(verify_api_key)])
async def get_stats(stats_repo: StatsRepository = Depends(get_stats_repo)):
    """Get usage statistics"""
    return await stats_repo.get_all_stats()
