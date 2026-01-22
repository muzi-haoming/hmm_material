"""
委托函 Schema
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.delegation import DelegationType, DelegationStatus


class DelegationBase(BaseModel):
    """委托函基础 Schema"""
    type: DelegationType
    amount: Decimal = Field(..., ge=0)
    content: str
    raw_material_info: Optional[str] = None
    expected_completion_date: Optional[datetime] = None
    remark: Optional[str] = None


class DelegationCreate(DelegationBase):
    """委托函创建 Schema"""
    order_id: int
    delegator_id: int   # 委托方（合同厂家）
    delegatee_id: int   # 被委托方（第三方厂家）


class DelegationUpdate(BaseModel):
    """委托函更新 Schema"""
    status: Optional[DelegationStatus] = None
    amount: Optional[Decimal] = Field(None, ge=0)
    content: Optional[str] = None
    raw_material_info: Optional[str] = None
    expected_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    remark: Optional[str] = None


class DelegationResponse(DelegationBase):
    """委托函响应 Schema"""
    id: int
    delegation_no: str
    status: DelegationStatus
    order_id: int
    delegator_id: int
    delegatee_id: int
    delegation_date: datetime
    actual_completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
