"""
安全模块 - JWT 令牌和密码处理
"""
from datetime import datetime, timedelta
from typing import Optional, Any
import hashlib

from jose import jwt

from .config import settings


def create_access_token(
    subject: str | Any,
    expires_delta: Optional[timedelta] = None
) -> str:
    """创建 JWT 访问令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码 (MD5)"""
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """获取密码哈希 (MD5)"""
    return hashlib.md5(password.encode('utf-8')).hexdigest()
