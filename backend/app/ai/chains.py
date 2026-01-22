"""
Langchain Chains - AI 业务链
"""
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from .prompts import (
    ORDER_ANALYSIS_PROMPT,
    DELEGATION_ADVICE_PROMPT,
    SUPPLY_CHAIN_OPTIMIZATION_PROMPT
)


class BaseChain:
    """基础 Chain 类"""

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
        self.output_parser = StrOutputParser()


class OrderAnalysisChain(BaseChain):
    """订单分析链 - 分析订单履行方式"""

    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_template(ORDER_ANALYSIS_PROMPT)
        self.chain = self.prompt | self.llm | self.output_parser

    async def analyze(
        self,
        order_info: Dict[str, Any],
        contract_manufacturer_info: Dict[str, Any],
        alternative_suppliers: List[Dict[str, Any]]
    ) -> str:
        """
        分析订单履行方式

        Args:
            order_info: 订单信息
            contract_manufacturer_info: 合同厂家信息
            alternative_suppliers: 替代厂家列表

        Returns:
            分析结果文本
        """
        result = await self.chain.ainvoke({
            "order_info": self._format_order_info(order_info),
            "contract_manufacturer_info": self._format_manufacturer_info(
                contract_manufacturer_info
            ),
            "alternative_suppliers": self._format_suppliers(alternative_suppliers)
        })
        return result

    def _format_order_info(self, order_info: Dict) -> str:
        """格式化订单信息"""
        items_str = "\n".join([
            f"  - {item.get('product_name', '未知产品')}: "
            f"数量 {item.get('quantity', 0)} {item.get('unit', '')}，"
            f"单价 {item.get('unit_price', 0)} 元"
            for item in order_info.get("items", [])
        ])
        return f"""
订单编号: {order_info.get('order_no', 'N/A')}
工地: {order_info.get('site_name', 'N/A')}
订单项目:
{items_str}
总金额: {order_info.get('total_amount', 0)} 元
期望交付日期: {order_info.get('expected_delivery_date', 'N/A')}
"""

    def _format_manufacturer_info(self, info: Dict) -> str:
        """格式化厂家信息"""
        products_str = "\n".join([
            f"  - {p.get('name', '未知')}: 库存 {p.get('stock', 'N/A')}，"
            f"价格 {p.get('price', 'N/A')} 元"
            for p in info.get("available_products", [])
        ])
        return f"""
厂家名称: {info.get('name', 'N/A')}
厂家类型: {info.get('type', 'N/A')}
可供应产品:
{products_str}
"""

    def _format_suppliers(self, suppliers: List[Dict]) -> str:
        """格式化替代厂家列表"""
        if not suppliers:
            return "暂无替代厂家"

        return "\n".join([
            f"- {s.get('name', '未知')}: "
            f"类型 {s.get('type', 'N/A')}，"
            f"价格 {s.get('price', 'N/A')} 元，"
            f"生产周期 {s.get('production_days', 'N/A')} 天"
            for s in suppliers
        ])


class DelegationAssistant(BaseChain):
    """委托函助手 - 帮助生成委托函内容"""

    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_template(DELEGATION_ADVICE_PROMPT)
        self.chain = self.prompt | self.llm | self.output_parser

    async def generate_delegation_content(
        self,
        delegation_type: str,
        order_info: Dict[str, Any],
        delegator_info: Dict[str, Any],
        delegatee_info: Dict[str, Any],
        amount: float,
        additional_info: str = ""
    ) -> str:
        """
        生成委托函内容

        Args:
            delegation_type: 委托类型 (supply/process)
            order_info: 订单信息
            delegator_info: 委托方信息
            delegatee_info: 被委托方信息
            amount: 委托金额
            additional_info: 额外说明

        Returns:
            生成的委托函内容
        """
        type_desc = "委托供货" if delegation_type == "supply" else "委托加工"

        result = await self.chain.ainvoke({
            "delegation_type": type_desc,
            "order_info": self._format_order_info(order_info),
            "delegator_info": self._format_company_info(delegator_info),
            "delegatee_info": self._format_company_info(delegatee_info),
            "amount": f"{amount:,.2f} 元",
            "additional_info": additional_info or "无"
        })
        return result

    def _format_order_info(self, order_info: Dict) -> str:
        """格式化订单信息"""
        items_str = "\n".join([
            f"  - {item.get('product_name', '未知产品')}: "
            f"数量 {item.get('quantity', 0)}，规格 {item.get('specification', 'N/A')}"
            for item in order_info.get("items", [])
        ])
        return f"""
订单编号: {order_info.get('order_no', 'N/A')}
收货地址: {order_info.get('delivery_address', 'N/A')}
联系人: {order_info.get('delivery_contact', 'N/A')}
联系电话: {order_info.get('delivery_phone', 'N/A')}
产品清单:
{items_str}
"""

    def _format_company_info(self, info: Dict) -> str:
        """格式化公司信息"""
        return f"""
公司名称: {info.get('name', 'N/A')}
地址: {info.get('address', 'N/A')}
联系人: {info.get('contact_name', 'N/A')}
联系电话: {info.get('contact_phone', 'N/A')}
银行账户: {info.get('bank_account', 'N/A')}
开户行: {info.get('bank_name', 'N/A')}
"""


class SupplyChainOptimizer(BaseChain):
    """供应链优化助手"""

    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_template(
            SUPPLY_CHAIN_OPTIMIZATION_PROMPT
        )
        self.chain = self.prompt | self.llm | self.output_parser

    async def get_optimization_advice(
        self,
        order_history: List[Dict],
        supplier_capacity: List[Dict],
        current_issues: str
    ) -> str:
        """获取供应链优化建议"""
        result = await self.chain.ainvoke({
            "order_history": self._format_order_history(order_history),
            "supplier_capacity": self._format_supplier_capacity(supplier_capacity),
            "current_issues": current_issues
        })
        return result

    def _format_order_history(self, history: List[Dict]) -> str:
        """格式化历史订单"""
        if not history:
            return "暂无历史数据"
        return "\n".join([
            f"- {h.get('date', 'N/A')}: {h.get('product', 'N/A')} "
            f"数量 {h.get('quantity', 0)}，供应商 {h.get('supplier', 'N/A')}"
            for h in history
        ])

    def _format_supplier_capacity(self, capacity: List[Dict]) -> str:
        """格式化供应商能力"""
        if not capacity:
            return "暂无数据"
        return "\n".join([
            f"- {c.get('name', 'N/A')}: "
            f"产能 {c.get('capacity', 'N/A')}，"
            f"交付准时率 {c.get('on_time_rate', 'N/A')}%"
            for c in capacity
        ])
