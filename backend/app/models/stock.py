"""
库存模型
"""
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from .product import Product


class Stock(Base):
    """库存模型"""
    __tablename__ = "stock"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    product: Mapped["Product"] = relationship("Product", back_populates="stock")

    def __repr__(self) -> str:
        return f"<Stock(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
