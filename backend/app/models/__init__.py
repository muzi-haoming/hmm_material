"""
数据库模型
"""
from .user import User, UserRole
from .site import Site
from .manufacturer import Manufacturer, ManufacturerGroup, ManufacturerGroupDetail
from .contract import Contract
from .product import Product
from .order import Order
from .stock import Stock
from .stock_out import StockOut
from .stock_in import StockIn
from .purchase import Purchase
from .statement import (
    Statement,
    StatementMaterialDetail,
    StatementOtherExpensesItem,
    StatementOtherExpensesDetail,
)

__all__ = [
    "User",
    "UserRole",
    "Site",
    "Manufacturer",
    "ManufacturerGroup",
    "ManufacturerGroupDetail",
    "Contract",
    "Product",
    "Order",
    "Stock",
    "StockOut",
    "StockIn",
    "Purchase",
    "Statement",
    "StatementMaterialDetail",
    "StatementOtherExpensesItem",
    "StatementOtherExpensesDetail",
]
