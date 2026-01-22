"""
产品 Schema
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.product import ProductCategory


class ProductBase(BaseModel):
    """产品基础 Schema"""
    name: str = Field(..., max_length=200)
    code: str = Field(..., max_length=50)
    category: ProductCategory = ProductCategory.FINISHED
    specification: Optional[str] = Field(None, max_length=500)
    unit: str = Field(..., max_length=20)
    description: Optional[str] = None
    reference_price: Optional[Decimal] = Field(None, ge=0)


class ProductCreate(ProductBase):
    """产品创建 Schema"""
    pass


class ProductUpdate(BaseModel):
    """产品更新 Schema"""
    name: Optional[str] = Field(None, max_length=200)
    category: Optional[ProductCategory] = None
    specification: Optional[str] = Field(None, max_length=500)
    unit: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = None
    reference_price: Optional[Decimal] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """产品响应 Schema"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ManufacturerProductCreate(BaseModel):
    """厂家产品关联创建"""
    manufacturer_id: int
    product_id: int
    price: Decimal = Field(..., ge=0)
    stock_quantity: Optional[Decimal] = Field(None, ge=0)
    is_available: bool = True
    production_days: Optional[int] = Field(None, ge=0)


class ManufacturerProductResponse(BaseModel):
    """厂家产品关联响应"""
    id: int
    manufacturer_id: int
    product_id: int
    price: Decimal
    stock_quantity: Optional[Decimal] = None
    is_available: bool
    production_days: Optional[int] = None
    product: ProductResponse

    class Config:
        from_attributes = True
