"""
订单管理 API
"""
from typing import Optional
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.order import Order, OrderItem, OrderStatus, OrderType
from app.models.site import Site
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


def generate_order_no() -> str:
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
    # 获取工地信息（从合同关联）
    from app.models.contract import Contract
    result = await db.execute(
        select(Contract).where(Contract.id == order_in.contract_id)
    )
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )

    # 提取订单明细
    items_data = order_in.items
    order_data = order_in.model_dump(exclude={"items"})

    # 创建订单
    order = Order(
        **order_data,
        order_no=generate_order_no(),
        site_id=contract.site_id,
        order_date=datetime.now()
    )

    # 计算订单总金额
    total_amount = Decimal("0")
    for item_data in items_data:
        amount = item_data.quantity * item_data.unit_price
        total_amount += amount

    order.total_amount = total_amount
    db.add(order)
    await db.flush()

    # 创建订单明细
    for item_data in items_data:
        amount = item_data.quantity * item_data.unit_price
        order_item = OrderItem(
            order_id=order.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            amount=amount,
            specification=item_data.specification,
            remark=item_data.remark
        )
        db.add(order_item)

    await db.commit()

    # 重新加载订单及关联
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order.id)
    )
    order = result.scalar_one()

    return order


@router.get("", response_model=PaginatedResponse[OrderResponse])
async def list_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[OrderStatus] = Query(None, description="订单状态"),
    order_type: Optional[OrderType] = Query(None, description="订单类型"),
    site_id: Optional[int] = Query(None, description="工地ID"),
    contract_id: Optional[int] = Query(None, description="合同ID"),
    manufacturer_id: Optional[int] = Query(None, description="厂家ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取订单列表"""
    query = select(Order).options(selectinload(Order.items))

    if keyword:
        query = query.where(Order.order_no.ilike(f"%{keyword}%"))
    if status:
        query = query.where(Order.status == status)
    if order_type:
        query = query.where(Order.order_type == order_type)
    if site_id:
        query = query.where(Order.site_id == site_id)
    if contract_id:
        query = query.where(Order.contract_id == contract_id)
    if manufacturer_id:
        query = query.where(Order.manufacturer_id == manufacturer_id)

    # 查询总数
    count_query = select(func.count(Order.id))
    if keyword:
        count_query = count_query.where(Order.order_no.ilike(f"%{keyword}%"))
    if status:
        count_query = count_query.where(Order.status == status)
    if order_type:
        count_query = count_query.where(Order.order_type == order_type)
    if site_id:
        count_query = count_query.where(Order.site_id == site_id)
    if contract_id:
        count_query = count_query.where(Order.contract_id == contract_id)
    if manufacturer_id:
        count_query = count_query.where(Order.manufacturer_id == manufacturer_id)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Order.id.desc())
    )
    orders = result.scalars().unique().all()

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
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
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
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
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


@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """确认订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有待处理的订单可以确认"
        )

    order.status = OrderStatus.CONFIRMED
    await db.commit()

    return {"message": "订单已确认"}


@router.post("/{order_id}/ship")
async def ship_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """发货"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status not in [OrderStatus.CONFIRMED, OrderStatus.PROCESSING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单状态不正确"
        )

    order.status = OrderStatus.SHIPPED
    await db.commit()

    return {"message": "订单已发货"}


@router.post("/{order_id}/complete")
async def complete_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """完成订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    order.status = OrderStatus.COMPLETED
    order.actual_delivery_date = datetime.now()
    await db.commit()

    return {"message": "订单已完成"}


@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """取消订单"""
    result = await db.execute(
        select(Order).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单已完成或已取消，无法再次取消"
        )

    order.status = OrderStatus.CANCELLED
    await db.commit()

    return {"message": "订单已取消"}
