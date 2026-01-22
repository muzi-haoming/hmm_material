"""
委托函管理 API
"""
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.delegation import Delegation, DelegationStatus, DelegationType
from app.models.order import Order, OrderType
from app.schemas.delegation import DelegationCreate, DelegationUpdate, DelegationResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


def generate_delegation_no() -> str:
    """生成委托函编号"""
    now = datetime.now()
    return f"DEL{now.strftime('%Y%m%d%H%M%S')}{now.microsecond // 1000:03d}"


@router.post("", response_model=DelegationResponse, status_code=status.HTTP_201_CREATED)
async def create_delegation(
    delegation_in: DelegationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    创建委托函

    用于处理以下两种情况：
    1. 委托供货（type=supply）：合同厂家委托第三方厂家直接发货
    2. 委托加工（type=process）：合同厂家提供原材料，委托第三方厂家加工后发货
    """
    # 验证订单是否存在
    result = await db.execute(
        select(Order).where(Order.id == delegation_in.order_id)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在"
        )

    # 创建委托函
    delegation = Delegation(
        **delegation_in.model_dump(),
        delegation_no=generate_delegation_no(),
        delegation_date=datetime.now()
    )
    db.add(delegation)

    # 更新订单类型
    if delegation_in.type == DelegationType.SUPPLY:
        order.order_type = OrderType.DELEGATED
    else:
        order.order_type = OrderType.PROCESSED

    # 设置实际发货方为被委托方
    order.actual_shipper_id = delegation_in.delegatee_id

    await db.commit()
    await db.refresh(delegation)

    return delegation


@router.get("", response_model=PaginatedResponse[DelegationResponse])
async def list_delegations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    type: Optional[DelegationType] = Query(None, description="委托类型"),
    status: Optional[DelegationStatus] = Query(None, description="委托状态"),
    delegator_id: Optional[int] = Query(None, description="委托方ID"),
    delegatee_id: Optional[int] = Query(None, description="被委托方ID"),
    order_id: Optional[int] = Query(None, description="订单ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取委托函列表"""
    query = select(Delegation)

    if keyword:
        query = query.where(Delegation.delegation_no.ilike(f"%{keyword}%"))
    if type:
        query = query.where(Delegation.type == type)
    if status:
        query = query.where(Delegation.status == status)
    if delegator_id:
        query = query.where(Delegation.delegator_id == delegator_id)
    if delegatee_id:
        query = query.where(Delegation.delegatee_id == delegatee_id)
    if order_id:
        query = query.where(Delegation.order_id == order_id)

    # 查询总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Delegation.id.desc())
    )
    delegations = result.scalars().all()

    return PaginatedResponse(
        items=delegations,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{delegation_id}", response_model=DelegationResponse)
async def get_delegation(
    delegation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取委托函详情"""
    result = await db.execute(
        select(Delegation).where(Delegation.id == delegation_id)
    )
    delegation = result.scalar_one_or_none()

    if not delegation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="委托函不存在"
        )

    return delegation


@router.put("/{delegation_id}", response_model=DelegationResponse)
async def update_delegation(
    delegation_id: int,
    delegation_in: DelegationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新委托函"""
    result = await db.execute(
        select(Delegation).where(Delegation.id == delegation_id)
    )
    delegation = result.scalar_one_or_none()

    if not delegation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="委托函不存在"
        )

    update_data = delegation_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(delegation, field, value)

    await db.commit()
    await db.refresh(delegation)

    return delegation


@router.post("/{delegation_id}/accept")
async def accept_delegation(
    delegation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """接受委托"""
    result = await db.execute(
        select(Delegation).where(Delegation.id == delegation_id)
    )
    delegation = result.scalar_one_or_none()

    if not delegation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="委托函不存在"
        )

    if delegation.status != DelegationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有待确认的委托函可以接受"
        )

    delegation.status = DelegationStatus.ACCEPTED
    await db.commit()

    return {"message": "委托已接受"}


@router.post("/{delegation_id}/reject")
async def reject_delegation(
    delegation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """拒绝委托"""
    result = await db.execute(
        select(Delegation).where(Delegation.id == delegation_id)
    )
    delegation = result.scalar_one_or_none()

    if not delegation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="委托函不存在"
        )

    if delegation.status != DelegationStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只有待确认的委托函可以拒绝"
        )

    delegation.status = DelegationStatus.REJECTED
    await db.commit()

    return {"message": "委托已拒绝"}


@router.post("/{delegation_id}/complete")
async def complete_delegation(
    delegation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """完成委托"""
    result = await db.execute(
        select(Delegation).where(Delegation.id == delegation_id)
    )
    delegation = result.scalar_one_or_none()

    if not delegation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="委托函不存在"
        )

    if delegation.status not in [DelegationStatus.ACCEPTED, DelegationStatus.IN_PROGRESS]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="委托状态不正确"
        )

    delegation.status = DelegationStatus.COMPLETED
    delegation.actual_completion_date = datetime.now()
    await db.commit()

    return {"message": "委托已完成"}
