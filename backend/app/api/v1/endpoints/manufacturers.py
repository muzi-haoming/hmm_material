"""
厂家管理 API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.manufacturer import Manufacturer, ManufacturerGroup, ManufacturerType
from app.schemas.manufacturer import (
    ManufacturerCreate, ManufacturerUpdate, ManufacturerResponse,
    ManufacturerGroupCreate, ManufacturerGroupResponse
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


# ==================== 厂家管理 ====================

@router.post("", response_model=ManufacturerResponse, status_code=status.HTTP_201_CREATED)
async def create_manufacturer(
    manufacturer_in: ManufacturerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建厂家"""
    # 检查编号是否已存在
    result = await db.execute(
        select(Manufacturer).where(Manufacturer.code == manufacturer_in.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="厂家编号已存在"
        )

    # 提取 group_ids
    group_ids = manufacturer_in.group_ids
    manufacturer_data = manufacturer_in.model_dump(exclude={"group_ids"})

    manufacturer = Manufacturer(**manufacturer_data)
    db.add(manufacturer)
    await db.flush()

    # 关联厂家组
    if group_ids:
        result = await db.execute(
            select(ManufacturerGroup).where(ManufacturerGroup.id.in_(group_ids))
        )
        groups = result.scalars().all()
        manufacturer.groups = list(groups)

    await db.commit()
    await db.refresh(manufacturer)

    return manufacturer


@router.get("", response_model=PaginatedResponse[ManufacturerResponse])
async def list_manufacturers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    type: Optional[ManufacturerType] = Query(None, description="厂家类型"),
    province: Optional[str] = Query(None, description="省份"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家列表"""
    query = select(Manufacturer)

    if keyword:
        query = query.where(
            Manufacturer.name.ilike(f"%{keyword}%") |
            Manufacturer.code.ilike(f"%{keyword}%")
        )
    if type:
        query = query.where(Manufacturer.type == type)
    if province:
        query = query.where(Manufacturer.province == province)

    # 查询总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Manufacturer.id.desc())
    )
    manufacturers = result.scalars().all()

    return PaginatedResponse(
        items=manufacturers,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{manufacturer_id}", response_model=ManufacturerResponse)
async def get_manufacturer(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家详情"""
    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家不存在"
        )

    return manufacturer


@router.put("/{manufacturer_id}", response_model=ManufacturerResponse)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer_in: ManufacturerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新厂家"""
    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家不存在"
        )

    update_data = manufacturer_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(manufacturer, field, value)

    await db.commit()
    await db.refresh(manufacturer)

    return manufacturer


@router.delete("/{manufacturer_id}")
async def delete_manufacturer(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除厂家"""
    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家不存在"
        )

    await db.delete(manufacturer)
    await db.commit()

    return {"message": "厂家已删除"}


# ==================== 厂家组管理 ====================

@router.post("/groups", response_model=ManufacturerGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_manufacturer_group(
    group_in: ManufacturerGroupCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建厂家组"""
    member_ids = group_in.member_ids
    group_data = group_in.model_dump(exclude={"member_ids"})

    group = ManufacturerGroup(**group_data)
    db.add(group)
    await db.flush()

    if member_ids:
        result = await db.execute(
            select(Manufacturer).where(Manufacturer.id.in_(member_ids))
        )
        members = result.scalars().all()
        group.members = list(members)

    await db.commit()
    await db.refresh(group)

    return group


@router.get("/groups", response_model=PaginatedResponse[ManufacturerGroupResponse])
async def list_manufacturer_groups(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家组列表"""
    # 查询总数
    total_result = await db.execute(select(func.count(ManufacturerGroup.id)))
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        select(ManufacturerGroup)
        .options(selectinload(ManufacturerGroup.members))
        .offset(offset)
        .limit(page_size)
        .order_by(ManufacturerGroup.id.desc())
    )
    groups = result.scalars().all()

    return PaginatedResponse(
        items=groups,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/groups/{group_id}", response_model=ManufacturerGroupResponse)
async def get_manufacturer_group(
    group_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家组详情"""
    result = await db.execute(
        select(ManufacturerGroup)
        .options(selectinload(ManufacturerGroup.members))
        .where(ManufacturerGroup.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家组不存在"
        )

    return group
