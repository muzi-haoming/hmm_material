"""
API V1 模块
"""
from fastapi import APIRouter
from .endpoints import auth, users, sites, manufacturers, contracts, products, orders

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(sites.router, prefix="/sites", tags=["工地管理"])
api_router.include_router(manufacturers.router, prefix="/manufacturers", tags=["厂家管理"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["合同管理"])
api_router.include_router(products.router, prefix="/products", tags=["产品管理"])
api_router.include_router(orders.router, prefix="/orders", tags=["订单管理"])
