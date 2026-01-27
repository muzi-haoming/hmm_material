"""
工地模型
"""
from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from .base import TimestampMixin

if TYPE_CHECKING:
    from .contract import Contract


class Site(Base, TimestampMixin):
    """工地模型"""
    __tablename__ = "site"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # 关系
    contracts: Mapped[list["Contract"]] = relationship("Contract", back_populates="site")

    def __repr__(self) -> str:
        return f"<Site(id={self.id}, code={self.code}, name={self.name})>"
