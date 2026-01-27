"""
产品模型
"""
from typing import Optional, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .order import Order
    from .stock import Stock


class Product(Base, TimestampMixin):
    """产品模型"""
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(19, 4), nullable=True)

    # 关系
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="product")
    stock: Mapped[Optional["Stock"]] = relationship("Stock", back_populates="product", uselist=False)

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, code={self.code}, name={self.name})>"
