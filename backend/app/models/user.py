"""
用户相关模型
"""
from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .contract import Contract


class UserRole(Base):
    """用户角色模型"""
    __tablename__ = "user_role"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 关系
    users: Mapped[list["User"]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<UserRole(id={self.id}, code={self.code}, name={self.name})>"


class User(Base, TimestampMixin):
    """用户模型"""
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(32), nullable=False)  # MD5 32位
    role_id: Mapped[str] = mapped_column(String(36), ForeignKey("user_role.id"), nullable=False)

    # 关系
    role: Mapped["UserRole"] = relationship("UserRole", back_populates="users")
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="agent")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, name={self.name})>"
