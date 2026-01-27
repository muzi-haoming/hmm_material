"""
入库模型
"""
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class StockIn(Base, TimestampMixin):
    """入库模型"""
    __tablename__ = "stock_in"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    order: Mapped["Order"] = relationship("Order", back_populates="stock_ins")
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return f"<StockIn(id={self.id}, code={self.code}, quantity={self.quantity})>"
