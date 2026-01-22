"""
厂家模型
"""
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey, Table, Column, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .contract import ContractManufacturer
    from .product import ManufacturerProduct
    from .order import Order
    from .delegation import Delegation


class ManufacturerType(str, Enum):
    """厂家类型"""
    SUPPLIER = "supplier"          # 供应商（直接发货）
    PROCESSOR = "processor"        # 加工厂
    BOTH = "both"                  # 两者兼备


# 厂家组成员关联表
manufacturer_group_members = Table(
    "manufacturer_group_members",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("manufacturer_groups.id"), primary_key=True),
    Column("manufacturer_id", Integer, ForeignKey("manufacturers.id"), primary_key=True)
)


class ManufacturerGroup(Base, TimestampMixin):
    """厂家组模型"""
    __tablename__ = "manufacturer_groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 代理人
    agent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # 关系
    members: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer",
        secondary=manufacturer_group_members,
        back_populates="groups"
    )

    def __repr__(self) -> str:
        return f"<ManufacturerGroup(id={self.id}, name={self.name})>"


class Manufacturer(Base, TimestampMixin):
    """厂家模型"""
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # 厂家编号
    type: Mapped[ManufacturerType] = mapped_column(
        SQLEnum(ManufacturerType),
        default=ManufacturerType.SUPPLIER
    )
    address: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100))
    province: Mapped[str] = mapped_column(String(100))
    contact_name: Mapped[str] = mapped_column(String(100))  # 联系人
    contact_phone: Mapped[str] = mapped_column(String(20))  # 联系电话
    bank_account: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # 银行账号
    bank_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # 开户行
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 代理人
    agent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # 关系
    agent: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="managed_manufacturers",
        foreign_keys=[agent_id]
    )

    groups: Mapped[List["ManufacturerGroup"]] = relationship(
        "ManufacturerGroup",
        secondary=manufacturer_group_members,
        back_populates="members"
    )

    contract_relations: Mapped[List["ContractManufacturer"]] = relationship(
        "ContractManufacturer",
        back_populates="manufacturer"
    )

    products: Mapped[List["ManufacturerProduct"]] = relationship(
        "ManufacturerProduct",
        back_populates="manufacturer"
    )

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="manufacturer",
        foreign_keys="Order.manufacturer_id"
    )

    # 作为委托方的委托函
    delegations_as_delegator: Mapped[List["Delegation"]] = relationship(
        "Delegation",
        back_populates="delegator",
        foreign_keys="Delegation.delegator_id"
    )

    # 作为被委托方的委托函
    delegations_as_delegatee: Mapped[List["Delegation"]] = relationship(
        "Delegation",
        back_populates="delegatee",
        foreign_keys="Delegation.delegatee_id"
    )

    def __repr__(self) -> str:
        return f"<Manufacturer(id={self.id}, name={self.name}, type={self.type})>"
