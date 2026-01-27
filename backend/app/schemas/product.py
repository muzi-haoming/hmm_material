"""
产品 Schema
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """产品基础 Schema"""
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    unit: str = Field(..., max_length=20)
    price: Optional[Decimal] = Field(None, ge=0)


class ProductCreate(ProductBase):
    """产品创建 Schema"""
    pass


class ProductUpdate(BaseModel):
    """产品更新 Schema"""
    code: Optional[str] = Field(None, max_length=50)
    name: Optional[str] = Field(None, max_length=200)
    unit: Optional[str] = Field(None, max_length=20)
    price: Optional[Decimal] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """产品响应 Schema"""
    id: str
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
