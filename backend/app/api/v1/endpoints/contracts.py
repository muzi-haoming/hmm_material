"""
合同管理 API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.contract import Contract, ContractManufacturer, ContractStatus
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.post("", response_model=ContractResponse, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract_in: ContractCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建合同"""
    # 检查合同编号是否已存在
    result = await db.execute(
        select(Contract).where(Contract.contract_no == contract_in.contract_no)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="合同编号已存在"
        )

    # 提取厂家关联数据
    manufacturers_data = contract_in.manufacturers
    contract_data = contract_in.model_dump(exclude={"manufacturers"})

    contract = Contract(**contract_data)
    db.add(contract)
    await db.flush()

    # 创建厂家关联
    for mfr_data in manufacturers_data:
        contract_mfr = ContractManufacturer(
            contract_id=contract.id,
            manufacturer_id=mfr_data.manufacturer_id,
            role_description=mfr_data.role_description,
            is_primary=mfr_data.is_primary
        )
        db.add(contract_mfr)

    await db.commit()

    # 重新加载合同及关联
    result = await db.execute(
        select(Contract)
        .options(selectinload(Contract.manufacturer_relations))
        .where(Contract.id == contract.id)
    )
    contract = result.scalar_one()

    return contract


@router.get("", response_model=PaginatedResponse[ContractResponse])
async def list_contracts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    status: Optional[ContractStatus] = Query(None, description="合同状态"),
    site_id: Optional[int] = Query(None, description="工地ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取合同列表"""
    query = select(Contract).options(selectinload(Contract.manufacturer_relations))

    if keyword:
        query = query.where(
            Contract.contract_no.ilike(f"%{keyword}%") |
            Contract.name.ilike(f"%{keyword}%")
        )
    if status:
        query = query.where(Contract.status == status)
    if site_id:
        query = query.where(Contract.site_id == site_id)

    # 查询总数
    count_query = select(func.count()).select_from(
        select(Contract.id).where(query.whereclause).subquery()
    ) if query.whereclause is not None else select(func.count(Contract.id))
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # 分页查询
    offset = (page - 1) * page_size
    result = await db.execute(
        query.offset(offset).limit(page_size).order_by(Contract.id.desc())
    )
    contracts = result.scalars().unique().all()

    return PaginatedResponse(
        items=contracts,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取合同详情"""
    result = await db.execute(
        select(Contract)
        .options(selectinload(Contract.manufacturer_relations))
        .where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )

    return contract


@router.put("/{contract_id}", response_model=ContractResponse)
async def update_contract(
    contract_id: int,
    contract_in: ContractUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新合同"""
    result = await db.execute(
        select(Contract)
        .options(selectinload(Contract.manufacturer_relations))
        .where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )

    update_data = contract_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contract, field, value)

    await db.commit()
    await db.refresh(contract)

    return contract


@router.delete("/{contract_id}")
async def delete_contract(
    contract_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除合同"""
    result = await db.execute(
        select(Contract).where(Contract.id == contract_id)
    )
    contract = result.scalar_one_or_none()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="合同不存在"
        )

    await db.delete(contract)
    await db.commit()

    return {"message": "合同已删除"}
