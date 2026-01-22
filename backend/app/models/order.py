"""
订单/发货模型
"""
from enum import Enum
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Text, ForeignKey, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .site import Site
    from .contract import Contract
    from .manufacturer import Manufacturer
    from .product import Product
    from .delegation import Delegation


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"              # 待处理
    CONFIRMED = "confirmed"          # 已确认
    PROCESSING = "processing"        # 处理中
    SHIPPED = "shipped"              # 已发货
    DELIVERED = "delivered"          # 已送达
    COMPLETED = "completed"          # 已完成
    CANCELLED = "cancelled"          # 已取消


class OrderType(str, Enum):
    """订单类型（对应三种发货情况）"""
    DIRECT = "direct"                # 直接发货
    DELEGATED = "delegated"          # 委托第三方发货
    PROCESSED = "processed"          # 加工后发货


class Order(Base, TimestampMixin):
    """订单模型"""
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_no: Mapped[str] = mapped_column(String(100), unique=True, index=True)  # 订单编号
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus),
        default=OrderStatus.PENDING
    )
    order_type: Mapped[OrderType] = mapped_column(
        SQLEnum(OrderType),
        default=OrderType.DIRECT
    )

    # 关联
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"))
    contract_id: Mapped[int] = mapped_column(ForeignKey("contracts.id"))
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))  # 合同厂家

    # 实际发货厂家（如果是委托/加工，可能与合同厂家不同）
    actual_shipper_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("manufacturers.id"),
        nullable=True
    )

    # 订单金额
    total_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)

    # 时间
    order_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    expected_delivery_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    actual_delivery_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # 收货地址（默认为工地地址，可修改）
    delivery_address: Mapped[str] = mapped_column(String(500))
    delivery_contact: Mapped[str] = mapped_column(String(100))
    delivery_phone: Mapped[str] = mapped_column(String(20))

    # 备注
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关系
    site: Mapped["Site"] = relationship("Site", back_populates="orders")
    contract: Mapped["Contract"] = relationship("Contract", back_populates="orders")
    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="orders",
        foreign_keys=[manufacturer_id]
    )
    actual_shipper: Mapped[Optional["Manufacturer"]] = relationship(
        "Manufacturer",
        foreign_keys=[actual_shipper_id]
    )

    items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    delegations: Mapped[List["Delegation"]] = relationship(
        "Delegation",
        back_populates="order"
    )

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, order_no={self.order_no}, status={self.status})>"


class OrderItem(Base, TimestampMixin):
    """订单明细模型"""
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 2))  # 数量
    unit_price: Mapped[Decimal] = mapped_column(Numeric(15, 2))  # 单价
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))  # 金额

    # 规格说明（可能与产品默认规格不同）
    specification: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")

    def __repr__(self) -> str:
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"
