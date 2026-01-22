"""
合同 Schema
"""
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field

from app.models.contract import ContractStatus


class ContractManufacturerCreate(BaseModel):
    """合同-厂家关联创建 Schema"""
    manufacturer_id: int
    role_description: Optional[str] = None
    is_primary: bool = False


class ContractBase(BaseModel):
    """合同基础 Schema"""
    contract_no: str = Field(..., max_length=100)
    name: str = Field(..., max_length=300)
    total_amount: Decimal = Field(default=0, ge=0)
    start_date: date
    end_date: date
    content: Optional[str] = None
    terms: Optional[str] = None


class ContractCreate(ContractBase):
    """合同创建 Schema"""
    site_id: int
    manufacturers: List[ContractManufacturerCreate]


class ContractUpdate(BaseModel):
    """合同更新 Schema"""
    name: Optional[str] = Field(None, max_length=300)
    status: Optional[ContractStatus] = None
    total_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    content: Optional[str] = None
    terms: Optional[str] = None


class ContractManufacturerResponse(BaseModel):
    """合同-厂家关联响应"""
    id: int
    manufacturer_id: int
    role_description: Optional[str] = None
    is_primary: bool

    class Config:
        from_attributes = True


class ContractResponse(ContractBase):
    """合同响应 Schema"""
    id: int
    status: ContractStatus
    site_id: int
    manufacturer_relations: List[ContractManufacturerResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
