"""
厂家相关模型
"""
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .stock_out import StockOut
    from .purchase import Purchase


class ManufacturerGroup(Base, TimestampMixin):
    """厂家组模型"""
    __tablename__ = "manufacturer_group"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 关系
    details: Mapped[list["ManufacturerGroupDetail"]] = relationship(
        "ManufacturerGroupDetail", back_populates="manufacturer_group"
    )
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="manufacturer_group")

    def __repr__(self) -> str:
        return f"<ManufacturerGroup(id={self.id}, code={self.code}, name={self.name})>"


class Manufacturer(Base, TimestampMixin):
    """厂家模型"""
    __tablename__ = "manufacturer"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 关系
    group_details: Mapped[list["ManufacturerGroupDetail"]] = relationship(
        "ManufacturerGroupDetail", back_populates="manufacturer"
    )
    stock_outs: Mapped[list["StockOut"]] = relationship("StockOut", back_populates="manufacturer")
    purchases_as_payer: Mapped[list["Purchase"]] = relationship(
        "Purchase", back_populates="payer_manufacturer", foreign_keys="Purchase.payer_manufacturer_id"
    )
    purchases_as_payee: Mapped[list["Purchase"]] = relationship(
        "Purchase", back_populates="payee_manufacturer", foreign_keys="Purchase.payee_manufacturer_id"
    )

    def __repr__(self) -> str:
        return f"<Manufacturer(id={self.id}, code={self.code}, name={self.name})>"


class ManufacturerGroupDetail(Base):
    """厂家组详情模型（厂家组-厂家关联）"""
    __tablename__ = "manufacturer_group_detail"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    manufacturer_group_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("manufacturer_group.id"), nullable=False
    )
    manufacturer_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("manufacturer.id"), nullable=False
    )

    # 关系
    manufacturer_group: Mapped["ManufacturerGroup"] = relationship(
        "ManufacturerGroup", back_populates="details"
    )
    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer", back_populates="group_details"
    )

    def __repr__(self) -> str:
        return f"<ManufacturerGroupDetail(group_id={self.manufacturer_group_id}, manufacturer_id={self.manufacturer_id})>"


# 避免循环导入
from .contract import Contract
