"""认证路由模块"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.auth.service import send_verification_code_service, register_service, login_service
from app.api.auth.dependencies import get_current_user, get_current_user_id
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.users import User, UserRole
import bcrypt
from app.api.auth.jwt import create_access_token

# 创建认证路由
router = APIRouter()


class SendCodeRequest(BaseModel):
    """发送验证码请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")


class UserCreate(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, description="邮箱验证码")
    avatar: Optional[str] = Field(None, description="头像图片路径")
    role: UserRole = Field(UserRole.USER, description="用户角色")


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: str
    avatar: Optional[str]
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """登录请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., description="密码")


class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str
    user: UserResponse


@router.post("/send-code/register", status_code=status.HTTP_200_OK)
async def send_verification_code(
    request: SendCodeRequest,
    db: AsyncSession = Depends(get_db)
):
    """发送注册邮箱验证码"""
    try:
        await send_verification_code_service(request.email, db)
        return {
            "message": "验证码已发送到您的邮箱"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册接口"""
    try:
        new_user = await register_service(user_data, db)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


from fastapi import Response

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    response: Response = Response()
):
    """用户登录接口"""
    try:
        user, access_token = await login_service(login_data.email, login_data.password, db)
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            avatar=user.avatar,
            role=user.role,
            is_active=user.is_active
        )
        
        # 设置 HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="lax",
            path="/"
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="Bearer",
            user=user_response
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return current_user


@router.get("/me/id", status_code=status.HTTP_200_OK)
async def get_current_user_id_info(
    user_id: int = Depends(get_current_user_id)
):
    """获取当前用户ID"""
    return {"user_id": user_id}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response
):
    """用户注销接口"""
    # 删除 HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value="",
        max_age=0,
        expires=0,
        path="/",
        httponly=True,
        samesite="Lax",
        # secure=False  # 本地开发
    )
    return {"msg": "退出成功"}


@router.post("/admin/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def admin_login(
    user_data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    """管理员登录接口"""
    # 从数据库获取用户
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar()
    
    # 验证用户是否存在、密码是否正确、是否为管理员
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    # 添加调试日志
    print(f"用户邮箱: {user.email}")
    print(f"用户角色: {user.role}")
    print(f"用户角色类型: {type(user.role)}")
    print(f"UserRole.ADMIN: {UserRole.ADMIN}")
    print(f"角色比较结果: {user.role == UserRole.ADMIN}")
    
    if not bcrypt.checkpw(user_data.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无管理员权限"
        )
    
    # 生成 JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 设置 HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="Lax",
        # secure=False  # 本地开发
    )
    
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.avatar,
        role=user.role,
        is_active=user.is_active
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )
