"""API 路由管理"""
from fastapi import APIRouter
from app.api.auth.router import router as auth_router
from app.api.users.router import router as users_router
from app.api.admin.router import router as admin_router
from app.api.books.router import router as books_router
from app.api.borrow.router import router as borrow_router

# 创建主路由
api_router = APIRouter()

# 包含认证相关路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])

# 包含用户相关路由
api_router.include_router(users_router, prefix="/users", tags=["用户"])

# 包含管理员相关路由
api_router.include_router(admin_router, prefix="/admin", tags=["管理员"])

# 包含图书相关路由
api_router.include_router(books_router, prefix="/books", tags=["图书"])

# 包含借阅相关路由
api_router.include_router(borrow_router, prefix="/borrow", tags=["借阅"])
