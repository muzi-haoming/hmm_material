"""
工地 Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    """工地基础 Schema"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    address: str = Field(..., max_length=500)
    city: str = Field(..., max_length=100)
    province: str = Field(..., max_length=100)
    contact_name: str = Field(..., max_length=100)
    contact_phone: str = Field(..., max_length=20)
    description: Optional[str] = None


class SiteCreate(SiteBase):
    """工地创建 Schema"""
    manager_id: Optional[int] = None


class SiteUpdate(BaseModel):
    """工地更新 Schema"""
    name: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    manager_id: Optional[int] = None


class SiteResponse(SiteBase):
    """工地响应 Schema"""
    id: int
    manager_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
