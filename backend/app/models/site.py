"""
工地模型
"""
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .contract import Contract
    from .order import Order


class Site(Base, TimestampMixin):
    """工地模型"""
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # 工地编号
    address: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100))
    province: Mapped[str] = mapped_column(String(100))
    contact_name: Mapped[str] = mapped_column(String(100))  # 联系人
    contact_phone: Mapped[str] = mapped_column(String(20))  # 联系电话
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 工地负责人
    manager_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    # 关系
    manager: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="managed_sites",
        foreign_keys=[manager_id]
    )

    contracts: Mapped[List["Contract"]] = relationship(
        "Contract",
        back_populates="site"
    )

    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="site"
    )

    def __repr__(self) -> str:
        return f"<Site(id={self.id}, name={self.name}, code={self.code})>"
