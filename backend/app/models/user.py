"""
用户模型
"""
from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .site import Site
    from .manufacturer import Manufacturer


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "ADMIN"              # 系统管理员
    SITE_MANAGER = "SITE_MANAGER"  # 工地管理员
    SITE_STAFF = "SITE_STAFF"    # 工地员工
    AGENT = "AGENT"              # 厂家代理人
    MANUFACTURER = "MANUFACTURER"  # 厂家员工


class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.SITE_STAFF
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # 关联的工地（如果是工地角色）
    site_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    # 关联的厂家（如果是厂家/代理人角色）
    manufacturer_id: Mapped[Optional[int]] = mapped_column(nullable=True)

    # 关系
    managed_sites: Mapped[List["Site"]] = relationship(
        "Site",
        back_populates="manager",
        foreign_keys="Site.manager_id"
    )

    managed_manufacturers: Mapped[List["Manufacturer"]] = relationship(
        "Manufacturer",
        back_populates="agent",
        foreign_keys="Manufacturer.agent_id"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"
