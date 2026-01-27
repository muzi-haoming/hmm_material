"""
结算单相关模型
"""
from datetime import datetime
from typing import TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .contract import Contract
    from .product import Product


class Statement(Base, TimestampMixin):
    """结算单模型"""
    __tablename__ = "statement"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    contract_id: Mapped[str] = mapped_column(String(36), ForeignKey("contract.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # 关系
    contract: Mapped["Contract"] = relationship("Contract", back_populates="statements")
    material_details: Mapped[list["StatementMaterialDetail"]] = relationship(
        "StatementMaterialDetail", back_populates="statement"
    )
    other_expenses_details: Mapped[list["StatementOtherExpensesDetail"]] = relationship(
        "StatementOtherExpensesDetail", back_populates="statement"
    )

    def __repr__(self) -> str:
        return f"<Statement(id={self.id}, code={self.code})>"


class StatementMaterialDetail(Base, TimestampMixin):
    """结算单物资明细模型"""
    __tablename__ = "statement_material_detail"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    statement_id: Mapped[str] = mapped_column(String(36), ForeignKey("statement.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String(36), ForeignKey("product.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    statement: Mapped["Statement"] = relationship("Statement", back_populates="material_details")
    product: Mapped["Product"] = relationship("Product")

    def __repr__(self) -> str:
        return f"<StatementMaterialDetail(id={self.id}, statement_id={self.statement_id})>"


class StatementOtherExpensesItem(Base, TimestampMixin):
    """结算单其他费用项模型"""
    __tablename__ = "statement_other_expenses_item"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 关系
    details: Mapped[list["StatementOtherExpensesDetail"]] = relationship(
        "StatementOtherExpensesDetail", back_populates="item"
    )

    def __repr__(self) -> str:
        return f"<StatementOtherExpensesItem(id={self.id}, code={self.code}, name={self.name})>"


class StatementOtherExpensesDetail(Base, TimestampMixin):
    """结算单其他费用明细模型"""
    __tablename__ = "statement_other_expenses_detail"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    statement_id: Mapped[str] = mapped_column(String(36), ForeignKey("statement.id"), nullable=False)
    item_id: Mapped[str] = mapped_column(String(36), ForeignKey("statement_other_expenses_item.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(19, 4), nullable=False)

    # 关系
    statement: Mapped["Statement"] = relationship("Statement", back_populates="other_expenses_details")
    item: Mapped["StatementOtherExpensesItem"] = relationship(
        "StatementOtherExpensesItem", back_populates="details"
    )

    def __repr__(self) -> str:
        return f"<StatementOtherExpensesDetail(id={self.id}, statement_id={self.statement_id})>"
