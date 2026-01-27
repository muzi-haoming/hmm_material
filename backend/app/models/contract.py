"""
合同模型
"""
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .site import Site
    from .manufacturer import ManufacturerGroup
    from .user import User
    from .order import Order
    from .statement import Statement


class Contract(Base, TimestampMixin):
    """合同模型"""
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    site_id: Mapped[int] = mapped_column(Integer, ForeignKey("site.id"), nullable=False)
    manufacturer_group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("manufacturer_group.id"), nullable=False
    )
    agent_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    status: Mapped[str] = mapped_column(CHAR(1), nullable=False)  # 状态：1-草稿 2-生效 3-完成 4-取消

    # 关系
    site: Mapped["Site"] = relationship("Site", back_populates="contracts")
    manufacturer_group: Mapped["ManufacturerGroup"] = relationship(
        "ManufacturerGroup", back_populates="contracts"
    )
    agent: Mapped["User"] = relationship("User", back_populates="contracts")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="contract")
    statements: Mapped[list["Statement"]] = relationship("Statement", back_populates="contract")

    def __repr__(self) -> str:
        return f"<Contract(id={self.id}, code={self.code}, name={self.name})>"
