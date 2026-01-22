"""
订单服务层
"""
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order import Order, OrderItem, OrderStatus, OrderType
from app.models.contract import Contract, ContractManufacturer
from app.models.manufacturer import Manufacturer
from app.models.product import ManufacturerProduct


class OrderService:
    """订单服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_manufacturer_can_supply(
        self,
        manufacturer_id: int,
        product_id: int,
        quantity: Decimal
    ) -> dict:
        """
        检查厂家是否能直接供应指定产品

        返回:
        {
            "can_supply": bool,
            "reason": str,
            "available_quantity": Decimal,
            "price": Decimal
        }
        """
        result = await self.db.execute(
            select(ManufacturerProduct)
            .where(ManufacturerProduct.manufacturer_id == manufacturer_id)
            .where(ManufacturerProduct.product_id == product_id)
            .where(ManufacturerProduct.is_available == True)
        )
        mp = result.scalar_one_or_none()

        if not mp:
            return {
                "can_supply": False,
                "reason": "厂家没有该产品",
                "available_quantity": Decimal("0"),
                "price": Decimal("0")
            }

        if mp.stock_quantity is not None and mp.stock_quantity < quantity:
            return {
                "can_supply": False,
                "reason": f"库存不足，当前库存: {mp.stock_quantity}",
                "available_quantity": mp.stock_quantity,
                "price": mp.price
            }

        return {
            "can_supply": True,
            "reason": "可以供应",
            "available_quantity": mp.stock_quantity or Decimal("999999"),
            "price": mp.price
        }

    async def find_alternative_suppliers(
        self,
        product_id: int,
        quantity: Decimal,
        exclude_manufacturer_id: Optional[int] = None
    ) -> List[dict]:
        """
        查找能提供指定产品的替代厂家

        返回可供应该产品的厂家列表，按价格排序
        """
        query = (
            select(ManufacturerProduct)
            .options(selectinload(ManufacturerProduct.manufacturer))
            .where(ManufacturerProduct.product_id == product_id)
            .where(ManufacturerProduct.is_available == True)
        )

        if exclude_manufacturer_id:
            query = query.where(
                ManufacturerProduct.manufacturer_id != exclude_manufacturer_id
            )

        result = await self.db.execute(query.order_by(ManufacturerProduct.price))
        mps = result.scalars().all()

        alternatives = []
        for mp in mps:
            # 检查库存是否充足
            if mp.stock_quantity is not None and mp.stock_quantity < quantity:
                continue

            alternatives.append({
                "manufacturer_id": mp.manufacturer_id,
                "manufacturer_name": mp.manufacturer.name if mp.manufacturer else "",
                "manufacturer_type": mp.manufacturer.type if mp.manufacturer else None,
                "price": mp.price,
                "stock_quantity": mp.stock_quantity,
                "production_days": mp.production_days
            })

        return alternatives

    async def determine_order_fulfillment(
        self,
        contract_id: int,
        items: List[dict]
    ) -> dict:
        """
        分析订单履行方式

        根据合同厂家的供应能力，决定订单的履行方式：
        1. 直接发货 (DIRECT)
        2. 委托第三方发货 (DELEGATED)
        3. 委托加工后发货 (PROCESSED)

        返回:
        {
            "fulfillment_type": OrderType,
            "items_analysis": [
                {
                    "product_id": int,
                    "quantity": Decimal,
                    "can_direct_supply": bool,
                    "alternative_suppliers": List[dict],
                    "recommendation": str
                }
            ],
            "recommendations": List[str]
        }
        """
        # 获取合同关联的主厂家
        result = await self.db.execute(
            select(ContractManufacturer)
            .where(ContractManufacturer.contract_id == contract_id)
            .where(ContractManufacturer.is_primary == True)
        )
        primary_cm = result.scalar_one_or_none()

        if not primary_cm:
            # 如果没有主厂家，取第一个
            result = await self.db.execute(
                select(ContractManufacturer)
                .where(ContractManufacturer.contract_id == contract_id)
            )
            primary_cm = result.scalar_one_or_none()

        if not primary_cm:
            return {
                "fulfillment_type": None,
                "items_analysis": [],
                "recommendations": ["合同没有关联厂家，无法履行订单"]
            }

        primary_manufacturer_id = primary_cm.manufacturer_id
        items_analysis = []
        all_can_supply = True
        recommendations = []

        for item in items:
            product_id = item["product_id"]
            quantity = Decimal(str(item["quantity"]))

            # 检查主厂家是否能供应
            supply_check = await self.check_manufacturer_can_supply(
                primary_manufacturer_id, product_id, quantity
            )

            # 查找替代厂家
            alternatives = await self.find_alternative_suppliers(
                product_id, quantity, primary_manufacturer_id
            )

            if supply_check["can_supply"]:
                recommendation = "合同厂家可直接供应"
            elif alternatives:
                all_can_supply = False
                # 检查是否有加工厂
                processors = [
                    a for a in alternatives
                    if a["manufacturer_type"] in ["processor", "both"]
                ]
                if processors:
                    recommendation = f"建议委托 {processors[0]['manufacturer_name']} 加工"
                else:
                    recommendation = f"建议委托 {alternatives[0]['manufacturer_name']} 供货"
            else:
                all_can_supply = False
                recommendation = "没有找到可供应的厂家"

            items_analysis.append({
                "product_id": product_id,
                "quantity": quantity,
                "can_direct_supply": supply_check["can_supply"],
                "supply_check": supply_check,
                "alternative_suppliers": alternatives,
                "recommendation": recommendation
            })

        # 确定履行类型
        if all_can_supply:
            fulfillment_type = OrderType.DIRECT
            recommendations.append("所有产品均可由合同厂家直接供应")
        else:
            # 检查是否需要加工
            needs_processing = any(
                any(
                    a["manufacturer_type"] in ["processor", "both"]
                    for a in item["alternative_suppliers"]
                )
                for item in items_analysis
                if not item["can_direct_supply"]
            )

            if needs_processing:
                fulfillment_type = OrderType.PROCESSED
                recommendations.append("部分产品需要第三方加工后发货")
            else:
                fulfillment_type = OrderType.DELEGATED
                recommendations.append("部分产品需要委托第三方厂家发货")

        return {
            "fulfillment_type": fulfillment_type,
            "items_analysis": items_analysis,
            "recommendations": recommendations,
            "primary_manufacturer_id": primary_manufacturer_id
        }
