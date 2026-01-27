"""
认证相关 API
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.username == form_data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)

    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user_in.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 创建用户
    user = User(
        id=str(uuid.uuid4()),
        name=user_in.name,
        username=user_in.username,
        password=get_password_hash(user_in.password),
        role_id=user_in.role_id
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 重新加载关联
    result = await db.execute(
        select(User)
        .options(selectinload(User.role))
        .where(User.id == user.id)
    )
    user = result.scalar_one()

    return user
