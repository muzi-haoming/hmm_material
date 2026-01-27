"""
合同 Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ContractBase(BaseModel):
    """合同基础 Schema"""
    code: str = Field(..., max_length=100)
    name: str = Field(..., max_length=200)
    site_id: int
    manufacturer_group_id: int
    agent_id: int
    status: str = Field(..., max_length=1)  # 状态：1-草稿 2-生效 3-完成 4-取消


class ContractCreate(ContractBase):
    """合同创建 Schema"""
    pass


class ContractUpdate(BaseModel):
    """合同更新 Schema"""
    code: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=200)
    site_id: Optional[int] = None
    manufacturer_group_id: Optional[int] = None
    agent_id: Optional[int] = None
    status: Optional[str] = Field(None, max_length=1)


class ContractResponse(ContractBase):
    """合同响应 Schema"""
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
