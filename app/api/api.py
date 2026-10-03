
# app/api/v1/api.py
from fastapi import APIRouter
 
# Import the individual routers
from app.api.auth import router as auth_router
from app.api.product import router as product_router 
from app.api.user import router as user_router
# Create the master v1 router
api_router = APIRouter()


api_router.include_router(auth_router)
api_router.include_router(product_router)
api_router.include_router(user_router)