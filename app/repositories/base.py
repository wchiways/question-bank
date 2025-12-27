"""基础仓储类 - 提供通用CRUD操作"""
from typing import Generic, TypeVar, Optional, List
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import get_logger

logger = get_logger(__name__)

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):
    """
    基础仓储类 - 提供通用CRUD操作

    Args:
        model: SQLModel模型类
        session: 异步数据库会话
    """

    def __init__(self, model: type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        """
        根据ID获取单个对象

        Args:
            id: 对象ID

        Returns:
            模型对象或None
        """
        return await self.session.get(self.model, id)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        获取所有对象（分页）

        Args:
            skip: 跳过的记录数
            limit: 返回的记录数限制

        Returns:
            模型对象列表
        """
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        """
        创建新对象

        Args:
            obj: 模型对象

        Returns:
            创建后的模型对象
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        logger.info(f"✅ 创建 {self.model.__name__}: {obj.id}")
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        """
        更新对象

        Args:
            obj: 模型对象

        Returns:
            更新后的模型对象
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        logger.info(f"✅ 更新 {self.model.__name__}: {obj.id}")
        return obj

    async def delete(self, id: int) -> bool:
        """
        删除对象

        Args:
            id: 对象ID

        Returns:
            删除成功返回True
        """
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            logger.info(f"✅ 删除 {self.model.__name__}: {id}")
            return True
        return False
