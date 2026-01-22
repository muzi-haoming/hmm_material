"""
委托函模型
"""
from enum import Enum
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Text, ForeignKey, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .manufacturer import Manufacturer


class DelegationType(str, Enum):
    """委托类型"""
    SUPPLY = "supply"      # 委托供货（情况2.1）
    PROCESS = "process"    # 委托加工（情况2.2）


class DelegationStatus(str, Enum):
    """委托函状态"""
    DRAFT = "draft"              # 草稿
    PENDING = "pending"          # 待确认
    ACCEPTED = "accepted"        # 已接受
    IN_PROGRESS = "in_progress"  # 执行中
    COMPLETED = "completed"      # 已完成
    REJECTED = "rejected"        # 已拒绝
    CANCELLED = "cancelled"      # 已取消


class Delegation(Base, TimestampMixin):
    """
    委托函模型

    用于处理以下两种情况：
    1. 委托供货：合同厂家委托第三方厂家直接发货
    2. 委托加工：合同厂家提供原材料，委托第三方厂家加工后发货
    """
    __tablename__ = "delegations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    delegation_no: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # 委托函编号
    type: Mapped[DelegationType] = mapped_column(SQLEnum(DelegationType))
    status: Mapped[DelegationStatus] = mapped_column(
        SQLEnum(DelegationStatus),
        default=DelegationStatus.DRAFT
    )

    # 关联订单
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))

    # 委托方（合同厂家）
    delegator_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))

    # 被委托方（第三方厂家）
    delegatee_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))

    # 委托金额（委托方支付给被委托方的款项）
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))

    # 委托内容描述
    content: Mapped[str] = mapped_column(Text)

    # 如果是加工委托，原材料信息
    raw_material_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 时间
    delegation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expected_completion_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    actual_completion_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # 备注
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="delegations")

    delegator: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="delegations_as_delegator",
        foreign_keys=[delegator_id]
    )

    delegatee: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="delegations_as_delegatee",
        foreign_keys=[delegatee_id]
    )

    def __repr__(self) -> str:
        return f"<Delegation(id={self.id}, delegation_no={self.delegation_no}, type={self.type})>"
