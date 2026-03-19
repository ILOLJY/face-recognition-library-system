"""API 路由管理"""
from fastapi import APIRouter
from app.api.auth.router import router as auth_router

# 创建主路由
api_router = APIRouter()

# 包含认证相关路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
