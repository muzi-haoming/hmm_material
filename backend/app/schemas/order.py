"""
订单 Schema
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    """订单基础 Schema"""
    code: str = Field(..., max_length=50)
    contract_id: int
    product_id: int
    quantity: Decimal = Field(..., gt=0)
    status: str = Field(..., max_length=1)  # 状态：1-待处理 2-处理中 3-完成 4-取消


class OrderCreate(OrderBase):
    """订单创建 Schema"""
    pass


class OrderUpdate(BaseModel):
    """订单更新 Schema"""
    code: Optional[str] = Field(None, max_length=50)
    contract_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[Decimal] = Field(None, gt=0)
    status: Optional[str] = Field(None, max_length=1)


class OrderResponse(OrderBase):
    """订单响应 Schema"""
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
