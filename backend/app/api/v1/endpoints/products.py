"""
产品管理 API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.product import Product, ManufacturerProduct, ProductCategory
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    ManufacturerProductCreate, ManufacturerProductResponse
)
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建产品"""
    # 检查编号是否已存在
    result = await db.execute(
        select(Product).where(Product.code == product_in.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="产品编号已存在"
        )

    product = Product(**product_in.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


@router.get("", response_model=PaginatedResponse[ProductResponse])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    category: Optional[ProductCategory] = Query(None, description="产品分类"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取产品列表"""
    query = select(Product)

    if keyword:
        query = query.where(
            Product.name.ilike(f"%{keyword}%") |
            Product.code.ilike(f"%{keyword}%")
        )
    if category:
        query = query.where(Product.category == category)

    # 查询总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Product.id.desc())
    )
    products = result.scalars().all()

    return PaginatedResponse(
        items=products,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取产品详情"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新产品"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除产品"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )

    await db.delete(product)
    await db.commit()

    return {"message": "产品已删除"}


# ==================== 厂家产品关联 ====================

@router.post("/manufacturer-products", status_code=status.HTTP_201_CREATED)
async def create_manufacturer_product(
    mp_in: ManufacturerProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建厂家-产品关联"""
    mp = ManufacturerProduct(**mp_in.model_dump())
    db.add(mp)
    await db.commit()
    await db.refresh(mp)

    return {"message": "关联创建成功", "id": mp.id}


@router.get("/manufacturer/{manufacturer_id}/products")
async def get_manufacturer_products(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取厂家可供应的产品列表"""
    result = await db.execute(
        select(ManufacturerProduct)
        .where(ManufacturerProduct.manufacturer_id == manufacturer_id)
        .where(ManufacturerProduct.is_available == True)
    )
    products = result.scalars().all()

    return {"items": products}
