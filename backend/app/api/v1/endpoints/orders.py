"""
订单管理 API
"""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


def generate_order_code() -> str:
    """生成订单编号"""
    now = datetime.now()
    return f"ORD{now.strftime('%Y%m%d%H%M%S')}{now.microsecond // 1000:03d}"


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建订单"""
    # 检查订单编号是否已存在
    result = await db.execute(
        select(Order).where(Order.code == order_in.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单编号已存在"
        )

    order = Order(**order_in.model_dump())
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return order


@router.get("", response_model=PaginatedResponse[OrderResponse])
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    order_status: Optional[str] = Query(None, description="订单状态"),
    contract_id: Optional[int] = Query(None, description="合同ID"),
    product_id: Optional[int] = Query(None, description="产品ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单列表"""
    query = select(Order)

    if keyword:
        query = query.where(Order.code.ilike(f"%{keyword}%"))
    if order_status:
        query = query.where(Order.status == order_status)
    if contract_id:
        query = query.where(Order.contract_id == contract_id)
    if product_id:
        query = query.where(Order.product_id == product_id)

    # 查询总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Order.id.desc())
    )
    orders = result.scalars().all()

    return PaginatedResponse(
        items=orders,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单详情"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    return order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    update_data = order_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)

    await db.commit()
    await db.refresh(order)

    return order


@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    await db.delete(order)
    await db.commit()

    return {"message": "订单已删除"}


# ==================== 状态变更 ====================

@router.post("/{order_id}/process")
async def process_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """处理订单（状态从1变为2）"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status != '1':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有待处理的订单可以开始处理"
        )

    order.status = '2'
    await db.commit()

    return {"message": "订单已开始处理"}


@router.post("/{order_id}/complete")
async def complete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """完成订单（状态变为3）"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status not in ['1', '2']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单状态不正确"
        )

    order.status = '3'
    await db.commit()

    return {"message": "订单已完成"}


@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """取消订单（状态变为4）"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status in ['3', '4']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单已完成或已取消，无法再次取消"
        )

    order.status = '4'
    await db.commit()

    return {"message": "订单已取消"}
