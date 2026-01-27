"""
工地管理 API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteUpdate, SiteResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED)
async def create_site(
    site_in: SiteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建工地"""
    # 检查编号是否已存在
    result = await db.execute(select(Site).where(Site.code == site_in.code))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="工地编号已存在"
        )

    site = Site(**site_in.model_dump())
    db.add(site)
    await db.commit()
    await db.refresh(site)

    return site


@router.get("", response_model=PaginatedResponse[SiteResponse])
async def list_sites(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取工地列表"""
    query = select(Site)

    # 搜索条件
    if keyword:
        query = query.where(
            Site.name.ilike(f"%{keyword}%") |
            Site.code.ilike(f"%{keyword}%")
        )

    # 查询总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Site.id.desc())
    )
    sites = result.scalars().all()

    return PaginatedResponse(
        items=sites,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{site_id}", response_model=SiteResponse)
async def get_site(
    site_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取工地详情"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工地不存在"
        )

    return site


@router.put("/{site_id}", response_model=SiteResponse)
async def update_site(
    site_id: int,
    site_in: SiteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新工地"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工地不存在"
        )

    update_data = site_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(site, field, value)

    await db.commit()
    await db.refresh(site)

    return site


@router.delete("/{site_id}")
async def delete_site(
    site_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除工地"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工地不存在"
        )

    await db.delete(site)
    await db.commit()

    return {"message": "工地已删除"}
