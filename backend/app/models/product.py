"""
产品/货物模型
"""
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from decimal import Decimal
from sqlalchemy import String, Text, ForeignKey, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .manufacturer import Manufacturer
    from .order import OrderItem


class ProductCategory(str, Enum):
    """产品分类"""
    RAW_MATERIAL = "raw_material"    # 原材料
    SEMI_FINISHED = "semi_finished"  # 半成品
    FINISHED = "finished"            # 成品
    OTHER = "other"                  # 其他


class Product(Base, TimestampMixin):
    """产品模型"""
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # 产品编号
    category: Mapped[ProductCategory] = mapped_column(
        SQLEnum(ProductCategory),
        default=ProductCategory.FINISHED
    )
    specification: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # 规格型号
    unit: Mapped[str] = mapped_column(String(20))  # 单位（吨、件、米等）
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 标准价格（参考）
    reference_price: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )

    # 关系
    manufacturer_products: Mapped[List["ManufacturerProduct"]] = relationship(
        "ManufacturerProduct",
        back_populates="product"
    )

    order_items: Mapped[List["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product"
    )

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, code={self.code})>"


class ManufacturerProduct(Base, TimestampMixin):
    """厂家-产品关联模型（厂家可供应的产品）"""
    __tablename__ = "manufacturer_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    # 该厂家的供应价格
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    # 库存数量（可选）
    stock_quantity: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 2),
        nullable=True
    )
    # 是否可供应
    is_available: Mapped[bool] = mapped_column(default=True)
    # 生产周期（天）
    production_days: Mapped[Optional[int]] = mapped_column(nullable=True)

    # 关系
    manufacturer: Mapped["Manufacturer"] = relationship(
        "Manufacturer",
        back_populates="products"
    )
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="manufacturer_products"
    )

    def __repr__(self) -> str:
        return f"<ManufacturerProduct(manufacturer_id={self.manufacturer_id}, product_id={self.product_id})>"
