"""
用户相关 Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserRoleBase(BaseModel):
    """用户角色基础 Schema"""
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)


class UserRoleResponse(UserRoleBase):
    """用户角色响应 Schema"""
    id: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """用户基础 Schema"""
    name: str = Field(..., max_length=200)
    username: str = Field(..., min_length=3, max_length=50)
    role_id: str


class UserCreate(UserBase):
    """用户创建 Schema"""
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """用户更新 Schema"""
    name: Optional[str] = Field(None, max_length=200)
    role_id: Optional[str] = None


class UserResponse(UserBase):
    """用户响应 Schema"""
    id: str
    create_time: datetime
    update_time: datetime
    role: Optional[UserRoleResponse] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录 Schema"""
    username: str
    password: str


class Token(BaseModel):
    """Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
