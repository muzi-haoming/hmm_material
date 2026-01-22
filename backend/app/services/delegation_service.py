"""
委托函服务层
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.delegation import Delegation, DelegationType, DelegationStatus
from app.models.order import Order, OrderType
from app.models.manufacturer import Manufacturer


class DelegationService:
    """委托函服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_delegation_no(self) -> str:
        """生成委托函编号"""
        now = datetime.now()
        return f"DEL{now.strftime('%Y%m%d%H%M%S')}{now.microsecond // 1000:03d}"

    async def create_supply_delegation(
        self,
        order_id: int,
        delegator_id: int,
        delegatee_id: int,
        amount: Decimal,
        content: str,
        expected_completion_date: datetime = None,
        remark: str = None
    ) -> Delegation:
        """
        创建委托供货函

        场景：合同厂家没有货物，委托第三方厂家直接发货
        """
        # 获取订单
        result = await self.db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("订单不存在")

        # 创建委托函
        delegation = Delegation(
            delegation_no=self.generate_delegation_no(),
            type=DelegationType.SUPPLY,
            status=DelegationStatus.PENDING,
            order_id=order_id,
            delegator_id=delegator_id,
            delegatee_id=delegatee_id,
            amount=amount,
            content=content,
            delegation_date=datetime.now(),
            expected_completion_date=expected_completion_date,
            remark=remark
        )
        self.db.add(delegation)

        # 更新订单类型和实际发货方
        order.order_type = OrderType.DELEGATED
        order.actual_shipper_id = delegatee_id

        await self.db.commit()
        await self.db.refresh(delegation)

        return delegation

    async def create_process_delegation(
        self,
        order_id: int,
        delegator_id: int,
        delegatee_id: int,
        amount: Decimal,
        content: str,
        raw_material_info: str,
        expected_completion_date: datetime = None,
        remark: str = None
    ) -> Delegation:
        """
        创建委托加工函

        场景：合同厂家有原材料，委托第三方厂家加工后发货
        """
        # 获取订单
        result = await self.db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("订单不存在")

        # 创建委托函
        delegation = Delegation(
            delegation_no=self.generate_delegation_no(),
            type=DelegationType.PROCESS,
            status=DelegationStatus.PENDING,
            order_id=order_id,
            delegator_id=delegator_id,
            delegatee_id=delegatee_id,
            amount=amount,
            content=content,
            raw_material_info=raw_material_info,
            delegation_date=datetime.now(),
            expected_completion_date=expected_completion_date,
            remark=remark
        )
        self.db.add(delegation)

        # 更新订单类型和实际发货方
        order.order_type = OrderType.PROCESSED
        order.actual_shipper_id = delegatee_id

        await self.db.commit()
        await self.db.refresh(delegation)

        return delegation

    async def accept_delegation(self, delegation_id: int) -> Delegation:
        """被委托方接受委托"""
        result = await self.db.execute(
            select(Delegation).where(Delegation.id == delegation_id)
        )
        delegation = result.scalar_one_or_none()
        if not delegation:
            raise ValueError("委托函不存在")

        if delegation.status != DelegationStatus.PENDING:
            raise ValueError("只有待确认的委托函可以接受")

        delegation.status = DelegationStatus.ACCEPTED
        await self.db.commit()
        await self.db.refresh(delegation)

        return delegation

    async def start_delegation(self, delegation_id: int) -> Delegation:
        """开始执行委托"""
        result = await self.db.execute(
            select(Delegation).where(Delegation.id == delegation_id)
        )
        delegation = result.scalar_one_or_none()
        if not delegation:
            raise ValueError("委托函不存在")

        if delegation.status != DelegationStatus.ACCEPTED:
            raise ValueError("只有已接受的委托函可以开始执行")

        delegation.status = DelegationStatus.IN_PROGRESS
        await self.db.commit()
        await self.db.refresh(delegation)

        return delegation

    async def complete_delegation(self, delegation_id: int) -> Delegation:
        """完成委托"""
        result = await self.db.execute(
            select(Delegation).where(Delegation.id == delegation_id)
        )
        delegation = result.scalar_one_or_none()
        if not delegation:
            raise ValueError("委托函不存在")

        if delegation.status not in [
            DelegationStatus.ACCEPTED,
            DelegationStatus.IN_PROGRESS
        ]:
            raise ValueError("委托状态不正确")

        delegation.status = DelegationStatus.COMPLETED
        delegation.actual_completion_date = datetime.now()
        await self.db.commit()
        await self.db.refresh(delegation)

        return delegation

    async def get_delegation_with_details(self, delegation_id: int) -> dict:
        """获取委托函详情（含关联信息）"""
        result = await self.db.execute(
            select(Delegation).where(Delegation.id == delegation_id)
        )
        delegation = result.scalar_one_or_none()
        if not delegation:
            return None

        # 获取委托方信息
        result = await self.db.execute(
            select(Manufacturer).where(Manufacturer.id == delegation.delegator_id)
        )
        delegator = result.scalar_one_or_none()

        # 获取被委托方信息
        result = await self.db.execute(
            select(Manufacturer).where(Manufacturer.id == delegation.delegatee_id)
        )
        delegatee = result.scalar_one_or_none()

        # 获取订单信息
        result = await self.db.execute(
            select(Order).where(Order.id == delegation.order_id)
        )
        order = result.scalar_one_or_none()

        return {
            "delegation": delegation,
            "delegator": delegator,
            "delegatee": delegatee,
            "order": order
        }
