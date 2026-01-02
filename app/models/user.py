"""User数据模型 - SQLModel定义"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Index

class UserBase(SQLModel):
    """User基础模型"""
    username: str = Field(index=True, max_length=50, unique=True, description="用户名")
    email: Optional[str] = Field(default=None, max_length=100, description="邮箱")
    is_active: bool = Field(default=True, description="是否激活")
    is_superuser: bool = Field(default=False, description="是否管理员")
    role: str = Field(default="user", max_length=20, description="角色")

class User(UserBase, table=True):
    """
    User数据库表模型
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(description="加密密码")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = Field(default=None, description="最后登录时间")

class UserCreate(UserBase):
    """创建User的请求模型"""
    password: str

class UserRead(UserBase):
    """读取User的响应模型"""
    id: int
    created_at: datetime
    last_login: Optional[datetime]

class UserUpdate(SQLModel):
    """更新User的请求模型"""
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    role: Optional[str] = None
    password: Optional[str] = None
