"""
出库模型
"""
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .manufacturer import Manufacturer
    from .product import Product


class StockOut(Base, TimestampMixin):
    """出库模型"""
    __tablename__ = "stock_out"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"), nullable=False)
    manufacturer_id: Mapped[int] = mapped_column(Integer, ForeignKey("manufacturer.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="stock_outs")
    manufacturer: Mapped["Manufacturer"] = relationship("Manufacturer", back_populates="stock_outs")
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return f"<StockOut(id={self.id}, code={self.code}, quantity={self.quantity})>"
