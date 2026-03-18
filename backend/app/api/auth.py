"""认证相关 API"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.users import User, UserRole
from app.models.face_data import FaceData
from app.cache.redis import get_redis
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

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


def generate_verification_code(length: int = 6) -> str:
    """生成验证码
    
    Args:
        length: 验证码长度
        
    Returns:
        str: 验证码
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


async def send_email(to_email: str, code: str):
    """发送验证码邮件
    
    Args:
        to_email: 收件人邮箱
        code: 验证码
    """
    # 邮件配置
    smtp_server = "smtp.163.com"
    smtp_port = 465
    sender_email = "lcz1421934734@163.com"
    sender_password = "WPvd5cQzrb7WZ36t"
    
    # 创建邮件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = "图书借阅系统 - 邮箱验证码"
    
    body = f"""
    尊敬的用户：
    
    您好！您正在注册图书借阅系统账号，您的验证码是：
    
    {code}
    
    验证码有效期为5分钟，请尽快完成注册。
    
    如果这不是您本人的操作，请忽略此邮件。
    
    图书借阅系统
    """
    
    message.attach(MIMEText(body, "plain", "utf-8"))
    
    # 发送邮件
    def send():
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())
    
    await asyncio.to_thread(send)


@router.post("/send-code/register", status_code=status.HTTP_200_OK)
async def send_verification_code(
    request: SendCodeRequest,
    db: AsyncSession = Depends(get_db)
):
    """发送注册邮箱验证码"""
    # 检查邮箱是否已被注册
    existing_email = await db.execute(
        select(User).where(User.email == request.email)
    )
    if existing_email.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    # 生成验证码
    code = generate_verification_code()
    
    # 将验证码存储到 Redis，5分钟过期
    redis_client = await get_redis()
    cache_key = f"verification_code:{request.email}"
    await redis_client.set(cache_key, code, expire=300)
    
    # 发送验证码邮件
    await send_email(request.email, code)
    
    # 开发环境直接返回验证码，生产环境请注释掉下面这行
    return {
        "message": "验证码已发送到您的邮箱"
    }


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册接口"""
    # 验证邮箱验证码
    redis_client = await get_redis()
    cache_key = f"verification_code:{user_data.email}"
    cached_code = await redis_client.get(cache_key)
    
    if not cached_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码已过期或不存在"
        )
    
    if cached_code != user_data.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误"
        )
    
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
    
    # 删除已使用的验证码
    await redis_client.delete(cache_key)
    
    # 为用户创建空的人脸数据记录
    face_data = FaceData(
        user_id=new_user.id,
        face_encoding=b'',  # 空的人脸特征
        face_image_path=None
    )
    
    db.add(face_data)
    await db.commit()
    
    return new_user
