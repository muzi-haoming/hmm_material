"""
厂家相关 Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ManufacturerBase(BaseModel):
    """厂家基础 Schema"""
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)


class ManufacturerCreate(ManufacturerBase):
    """厂家创建 Schema"""
    pass


class ManufacturerUpdate(BaseModel):
    """厂家更新 Schema"""
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=200)


class ManufacturerResponse(ManufacturerBase):
    """厂家响应 Schema"""
    id: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


class ManufacturerGroupBase(BaseModel):
    """厂家组基础 Schema"""
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)


class ManufacturerGroupCreate(ManufacturerGroupBase):
    """厂家组创建 Schema"""
    manufacturer_ids: Optional[List[str]] = None


class ManufacturerGroupUpdate(BaseModel):
    """厂家组更新 Schema"""
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=200)


class ManufacturerGroupResponse(ManufacturerGroupBase):
    """厂家组响应 Schema"""
    id: str
    create_time: datetime
    update_time: datetime
    manufacturers: List[ManufacturerResponse] = []

    class Config:
        from_attributes = True
