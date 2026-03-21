"""用户接口模块"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.auth.dependencies import get_current_user
from app.models.users import User
from pydantic import BaseModel, Field
from typing import Optional
import bcrypt
import os
from datetime import datetime

# 创建用户路由
router = APIRouter()


class UpdateUsernameRequest(BaseModel):
    """修改用户名请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="新用户名")


class UpdatePasswordRequest(BaseModel):
    """修改密码请求模型"""
    old_password: str = Field(..., min_length=6, description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: str
    avatar: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.get("/profile", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_profile(
    current_user: User = Depends(get_current_user)
):
    """获取用户个人信息"""
    return current_user


@router.put("/profile/username", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_username(
    request: UpdateUsernameRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改用户名"""
    # 检查用户名是否已存在
    from sqlalchemy import select
    existing_user = await db.execute(
        select(User).where(User.username == request.username, User.id != current_user.id)
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 更新用户名
    current_user.username = request.username
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.put("/profile/password", status_code=status.HTTP_200_OK)
async def update_password(
    request: UpdatePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改密码"""
    # 打印当前用户信息
    print("当前用户ID:", current_user.id)
    print("当前用户邮箱:", current_user.email)
    
    # 验证旧密码
    if not bcrypt.checkpw(
        request.old_password.encode('utf-8'), 
        current_user.password.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 加密新密码
    hashed_password = bcrypt.hashpw(
        request.new_password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')
    
    # 更新密码
    current_user.password = hashed_password
    await db.commit()
    
    return {"msg": "密码修改成功"}


@router.post("/profile/avatar", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """上传头像"""
    # 检查文件类型
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请上传图片文件"
        )
    
    # 确保上传目录存在
    upload_dir = "app/static/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成文件名
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{current_user.id}_{datetime.now().timestamp()}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # 保存文件
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="文件上传失败"
        )
    
    # 更新用户头像路径
    avatar_path = f"/static/avatars/{filename}"
    current_user.avatar = avatar_path
    await db.commit()
    await db.refresh(current_user)
    
    return current_user