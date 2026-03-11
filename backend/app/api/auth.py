"""认证相关 API"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.users import User, UserRole
from app.models.face_data import FaceData
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import bcrypt

# 创建认证路由
router = APIRouter()


class UserCreate(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, description="密码")
    email: EmailStr = Field(..., description="邮箱地址")
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


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册接口"""
    # 检查用户名是否已存在
    existing_user = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    existing_email = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_email.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 密码加密
    hashed_password = bcrypt.hashpw(
        user_data.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # 创建用户
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        email=user_data.email,
        avatar=user_data.avatar,
        role=user_data.role,
        is_active=True
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # 为用户创建空的人脸数据记录
    face_data = FaceData(
        user_id=new_user.id,
        face_encoding=b'',  # 空的人脸特征
        face_image_path=None
    )
    
    db.add(face_data)
    await db.commit()
    
    return new_user
