from typing import Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base import BaseRepository
from app.core.security import get_password_hash
from app.core.logger import get_logger

logger = get_logger(__name__)

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def find_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()
    
    async def find_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_user(self, user_in) -> User:
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
            role=user_in.role
        )
        return await self.create(db_user)
