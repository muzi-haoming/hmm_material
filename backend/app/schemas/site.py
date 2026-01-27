"""
工地 Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    """工地基础 Schema"""
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)


class SiteCreate(SiteBase):
    """工地创建 Schema"""
    pass


class SiteUpdate(BaseModel):
    """工地更新 Schema"""
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=200)


class SiteResponse(SiteBase):
    """工地响应 Schema"""
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
