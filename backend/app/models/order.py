"""
订单模型
"""
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Integer, ForeignKey, Numeric, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .contract import Contract
    from .product import Product
    from .stock_out import StockOut
    from .stock_in import StockIn
    from .purchase import Purchase


class Order(Base, TimestampMixin):
    """订单模型"""
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    contract_id: Mapped[int] = mapped_column(Integer, ForeignKey("contract.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)
    status: Mapped[str] = mapped_column(CHAR(1), nullable=False)  # 状态：1-待处理 2-处理中 3-完成 4-取消

    # 关系
    contract: Mapped["Contract"] = relationship("Contract", back_populates="orders")
    product: Mapped["Product"] = relationship("Product", back_populates="orders")
    stock_outs: Mapped[list["StockOut"]] = relationship("StockOut", back_populates="order")
    stock_ins: Mapped[list["StockIn"]] = relationship("StockIn", back_populates="order")
    purchases: Mapped[list["Purchase"]] = relationship("Purchase", back_populates="order")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, code={self.code}, status={self.status})>"
