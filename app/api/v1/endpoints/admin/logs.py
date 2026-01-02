from fastapi import APIRouter, HTTPException, Query
from app.core.config import settings
import os

router = APIRouter()

@router.get("/")
async def get_logs(
    lines: int = Query(100, ge=1, le=1000),
    keyword: str = Query(None)
):
    """获取系统日志"""
    log_file = settings.logging.file
    if not os.path.exists(log_file):
        return {"logs": [], "message": "Log file not found"}
    
    try:
        # 简单读取最后N行
        # 在生产环境中，建议使用更高效的日志系统或专门的日志库
        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            all_lines = f.readlines()
            
        if keyword:
            all_lines = [line for line in all_lines if keyword.lower() in line.lower()]
            
        selected_lines = all_lines[-lines:]
        # 反转顺序，最新的在前
        selected_lines.reverse()
        
        return {
            "logs": selected_lines,
            "total": len(all_lines)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))