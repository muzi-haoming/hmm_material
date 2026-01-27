"""
厂家管理 API
"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.manufacturer import Manufacturer, ManufacturerGroup, ManufacturerGroupDetail
from app.schemas.manufacturer import (
    ManufacturerCreate, ManufacturerUpdate, ManufacturerResponse,
    ManufacturerGroupCreate, ManufacturerGroupUpdate, ManufacturerGroupResponse
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

    manufacturer = Manufacturer(id=str(uuid.uuid4()), **manufacturer_in.model_dump())
    db.add(manufacturer)
    await db.commit()
    await db.refresh(manufacturer)

    return manufacturer


@router.get("", response_model=PaginatedResponse[ManufacturerResponse])
async def list_manufacturers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
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
    manufacturer_id: str,
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
    manufacturer_id: str,
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
    manufacturer_id: str,
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
    # 检查编号是否已存在
    result = await db.execute(
        select(ManufacturerGroup).where(ManufacturerGroup.code == group_in.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="厂家组编号已存在"
        )

    manufacturer_ids = group_in.manufacturer_ids or []
    group_data = group_in.model_dump(exclude={"manufacturer_ids"})

    group = ManufacturerGroup(id=str(uuid.uuid4()), **group_data)
    db.add(group)
    await db.flush()

    # 添加厂家关联
    for manufacturer_id in manufacturer_ids:
        detail = ManufacturerGroupDetail(
            id=str(uuid.uuid4()),
            manufacturer_group_id=group.id,
            manufacturer_id=manufacturer_id
        )
        db.add(detail)

    await db.commit()

    # 重新加载以获取关联数据
    result = await db.execute(
        select(ManufacturerGroup)
        .options(selectinload(ManufacturerGroup.details).selectinload(ManufacturerGroupDetail.manufacturer))
        .where(ManufacturerGroup.id == group.id)
    )
    group = result.scalar_one()

    # 构建响应
    return _build_group_response(group)


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
        .options(selectinload(ManufacturerGroup.details).selectinload(ManufacturerGroupDetail.manufacturer))
        .offset(offset)
        .limit(page_size)
        .order_by(ManufacturerGroup.id.desc())
    )
    groups = result.scalars().all()

    # 构建响应
    items = [_build_group_response(g) for g in groups]

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/groups/{group_id}", response_model=ManufacturerGroupResponse)
async def get_manufacturer_group(
    group_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家组详情"""
    result = await db.execute(
        select(ManufacturerGroup)
        .options(selectinload(ManufacturerGroup.details).selectinload(ManufacturerGroupDetail.manufacturer))
        .where(ManufacturerGroup.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家组不存在"
        )

    return _build_group_response(group)


@router.put("/groups/{group_id}", response_model=ManufacturerGroupResponse)
async def update_manufacturer_group(
    group_id: str,
    group_in: ManufacturerGroupUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新厂家组"""
    result = await db.execute(
        select(ManufacturerGroup).where(ManufacturerGroup.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家组不存在"
        )

    update_data = group_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)

    await db.commit()

    # 重新加载
    result = await db.execute(
        select(ManufacturerGroup)
        .options(selectinload(ManufacturerGroup.details).selectinload(ManufacturerGroupDetail.manufacturer))
        .where(ManufacturerGroup.id == group_id)
    )
    group = result.scalar_one()

    return _build_group_response(group)


@router.delete("/groups/{group_id}")
async def delete_manufacturer_group(
    group_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除厂家组"""
    result = await db.execute(
        select(ManufacturerGroup).where(ManufacturerGroup.id == group_id)
    )
    group = result.scalar_one_or_none()

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="厂家组不存在"
        )

    # 删除关联详情
    await db.execute(
        ManufacturerGroupDetail.__table__.delete().where(
            ManufacturerGroupDetail.manufacturer_group_id == group_id
        )
    )

    await db.delete(group)
    await db.commit()

    return {"message": "厂家组已删除"}


def _build_group_response(group: ManufacturerGroup) -> dict:
    """构建厂家组响应"""
    manufacturers = [
        ManufacturerResponse.model_validate(detail.manufacturer)
        for detail in group.details
        if detail.manufacturer
    ]
    return ManufacturerGroupResponse(
        id=group.id,
        code=group.code,
        name=group.name,
        create_time=group.create_time,
        update_time=group.update_time,
        manufacturers=manufacturers
    )
