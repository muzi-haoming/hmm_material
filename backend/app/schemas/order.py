"""
订单 Schema
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.order import OrderStatus, OrderType


class OrderItemCreate(BaseModel):
    """订单明细创建 Schema"""
    product_id: int
    quantity: Decimal = Field(..., gt=0)
    unit_price: Decimal = Field(..., ge=0)
    specification: Optional[str] = Field(None, max_length=500)
    remark: Optional[str] = None


class OrderItemResponse(BaseModel):
    """订单明细响应 Schema"""
    id: int
    product_id: int
    quantity: Decimal
    unit_price: Decimal
    amount: Decimal
    specification: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """订单基础 Schema"""
    delivery_address: str = Field(..., max_length=500)
    delivery_contact: str = Field(..., max_length=100)
    delivery_phone: str = Field(..., max_length=20)
    expected_delivery_date: Optional[datetime] = None
    remark: Optional[str] = None


class OrderCreate(OrderBase):
    """订单创建 Schema"""
    contract_id: int
    manufacturer_id: int
    order_type: OrderType = OrderType.DIRECT
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    """订单更新 Schema"""
    status: Optional[OrderStatus] = None
    order_type: Optional[OrderType] = None
    actual_shipper_id: Optional[int] = None
    delivery_address: Optional[str] = Field(None, max_length=500)
    delivery_contact: Optional[str] = Field(None, max_length=100)
    delivery_phone: Optional[str] = Field(None, max_length=20)
    expected_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    remark: Optional[str] = None


class OrderResponse(OrderBase):
    """订单响应 Schema"""
    id: int
    order_no: str
    status: OrderStatus
    order_type: OrderType
    site_id: int
    contract_id: int
    manufacturer_id: int
    actual_shipper_id: Optional[int] = None
    total_amount: Decimal
    order_date: datetime
    actual_delivery_date: Optional[datetime] = None
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
