"""
合同模型
"""
from enum import Enum
from datetime import date
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Text, ForeignKey, Date, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .site import Site
    from .manufacturer import Manufacturer
    from .order import Order


class ContractStatus(str, Enum):
    """合同状态"""
    DRAFT = "draft"          # 草稿
    ACTIVE = "active"        # 生效中
    COMPLETED = "completed"  # 已完成
    CANCELLED = "cancelled"  # 已取消
    EXPIRED = "expired"      # 已过期


class Contract(Base, TimestampMixin):
    """合同模型"""
    __tablename__ = "contracts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_no: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # 合同编号
    name: Mapped[str] = mapped_column(String(300))  # 合同名称
    status: Mapped[ContractStatus] = mapped_column(
        SQLEnum(ContractStatus),
        default=ContractStatus.DRAFT
    )

    # 关联工地
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))

    # 合同金额
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)

    # 合同期限
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)

    # 合同内容
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 合同条款

    # 关系
    site: Mapped["Site"] = relationship("Site", back_populates="contracts")

    manufacturer_relations: Mapped[List["ContractManufacturer"]] = relationship(
        "ContractManufacturer",
        back_populates="contract",
        cascade="all, delete-orphan"
    )

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="contract"
    )

    def __repr__(self) -> str:
        return f"<Contract(id={self.id}, contract_no={self.contract_no})>"


class ContractManufacturer(Base, TimestampMixin):
    """合同-厂家关联模型（多对多中间表，带额外字段）"""
    __tablename__ = "contract_manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))

    # 该厂家在合同中的角色/备注
    role_description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    is_primary: Mapped[bool] = mapped_column(default=False)  # 是否为主供应商

    # 关系
    contract: Mapped["Contract"] = relationship(
        "Contract",
        back_populates="manufacturer_relations"
    )
    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="contract_relations"
    )

    def __repr__(self) -> str:
        return f"<ContractManufacturer(contract_id={self.contract_id}, manufacturer_id={self.manufacturer_id})>"
