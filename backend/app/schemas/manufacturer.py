"""
厂家 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.manufacturer import ManufacturerType


class ManufacturerBase(BaseModel):
    """厂家基础 Schema"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    type: ManufacturerType = ManufacturerType.SUPPLIER
    address: str = Field(..., max_length=500)
    city: str = Field(..., max_length=100)
    province: str = Field(..., max_length=100)
    contact_name: str = Field(..., max_length=100)
    contact_phone: str = Field(..., max_length=20)
    bank_account: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None


class ManufacturerCreate(ManufacturerBase):
    """厂家创建 Schema"""
    agent_id: Optional[int] = None
    group_ids: Optional[List[int]] = None


class ManufacturerUpdate(BaseModel):
    """厂家更新 Schema"""
    name: Optional[str] = Field(None, max_length=200)
    type: Optional[ManufacturerType] = None
    address: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    province: Optional[str] = Field(None, max_length=100)
    contact_name: Optional[str] = Field(None, max_length=100)
    contact_phone: Optional[str] = Field(None, max_length=20)
    bank_account: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    agent_id: Optional[int] = None


class ManufacturerResponse(ManufacturerBase):
    """厂家响应 Schema"""
    id: int
    agent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ManufacturerGroupBase(BaseModel):
    """厂家组基础 Schema"""
    name: str = Field(..., max_length=200)
    description: Optional[str] = None


class ManufacturerGroupCreate(ManufacturerGroupBase):
    """厂家组创建 Schema"""
    agent_id: Optional[int] = None
    member_ids: Optional[List[int]] = None


class ManufacturerGroupResponse(ManufacturerGroupBase):
    """厂家组响应 Schema"""
    id: int
    agent_id: Optional[int] = None
    members: List[ManufacturerResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
