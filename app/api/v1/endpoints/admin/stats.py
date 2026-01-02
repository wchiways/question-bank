from fastapi import APIRouter, Depends
from app.api import deps
from app.repositories.question_repository import QuestionRepository
from sqlmodel import select, func
import os
from app.core.config import settings
from app.models.question import Question

router = APIRouter()

@router.get("/")
async def get_stats(
    question_repo: QuestionRepository = Depends(deps.get_question_repo)
):
    """获取系统综合统计信息"""

    # DB Counts
    q_count = await question_repo.session.execute(select(func.count()).select_from(Question))

    # Log Size
    log_size = 0
    if os.path.exists(settings.logging.file):
        log_size = os.path.getsize(settings.logging.file)

    return {
        "questions_total": q_count.scalar_one(),
        "log_size_bytes": log_size,
        "ai_provider": settings.ai.default_provider,
        "debug_mode": settings.app.debug
    }