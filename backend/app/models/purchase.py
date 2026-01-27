"""
采购单模型
"""
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .user import User
    from .manufacturer import Manufacturer
    from .product import Product


class Purchase(Base, TimestampMixin):
    """采购单模型"""
    __tablename__ = "purchase"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("order.id"), nullable=False)
    purchaser: Mapped[str] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
    payer_manufacturer_id: Mapped[str] = mapped_column(String(36), ForeignKey("manufacturer.id"), nullable=False)
    payee_manufacturer_id: Mapped[str] = mapped_column(String(36), ForeignKey("manufacturer.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="purchases")
    purchaser_user: Mapped["User"] = relationship("User")
    payer_manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer", foreign_keys=[payer_manufacturer_id], back_populates="purchases_as_payer"
    )
    payee_manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer", foreign_keys=[payee_manufacturer_id], back_populates="purchases_as_payee"
    )
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return f"<Purchase(id={self.id}, code={self.code}, amount={self.amount})>"
