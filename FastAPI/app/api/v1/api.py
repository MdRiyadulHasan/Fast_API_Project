# app/api/v1/api.py
from fastapi import APIRouter
from app.vendor.routes import router as vendor_router
# from app.products.routes import router as product_router
# from app.auth.routes import router as auth_router
# from app.orders.routes import router as order_router

api_router = APIRouter()
api_router.include_router(vendor_router, prefix="/vendor", tags=["Vendors"])
# api_router.include_router(product_router, prefix="/products", tags=["Products"])
# api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# api_router.include_router(order_router, prefix="/orders", tags=["Orders"])
