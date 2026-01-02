from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.api import deps
from app.repositories.question_repository import QuestionRepository
from fastapi import Depends
from sqlmodel import select, func
import os
import shutil
from datetime import datetime
from app.models.question import Question
from app.models.user import User

router = APIRouter()

@router.get("/stats")
async def get_db_stats(
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """获取数据库统计信息"""
    db_url = settings.database.url
    if "sqlite" in db_url:
        db_path = db_url.replace("sqlite+aiosqlite:///", "")
        size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        size_mb = round(size / (1024 * 1024), 2)
    else:
        size_mb = 0 # Not supported for other DBs yet

    # Count rows
    q_count = await question_repo.session.execute(select(func.count()).select_from(Question))
    u_count = await question_repo.session.execute(select(func.count()).select_from(User))

    return {
        "type": settings.database.url.split(":")[0],
        "size_mb": size_mb,
        "questions": q_count.scalar_one(),
        "users": u_count.scalar_one()
    }

@router.post("/backup")
async def backup_database():
    """备份数据库 (仅限SQLite)"""
    db_url = settings.database.url
    if "sqlite" not in db_url:
        raise HTTPException(status_code=400, detail="Only SQLite backup is supported currently")
    
    db_path = db_url.replace("sqlite+aiosqlite:///", "")
    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="Database file not found")
        
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"backup_{timestamp}.db")
    
    try:
        shutil.copy2(db_path, backup_path)
        return {"message": "Backup successful", "path": backup_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))