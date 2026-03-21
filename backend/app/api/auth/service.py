"""认证服务模块"""
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio
import os
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.users import User, UserRole
from app.models.face_data import FaceData
from app.cache.redis import get_redis
from app.api.auth.jwt import create_access_token


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
    sender_password = os.getenv("SMTP_PASSWORD")

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


async def send_verification_code_service(email: str, db: AsyncSession):
    """发送验证码服务
    
    Args:
        email: 邮箱地址
        db: 数据库会话
    
    Raises:
        ValueError: 邮箱已被注册
    """
    # 检查邮箱是否已被注册
    existing_email = await db.execute(
        select(User).where(User.email == email)
    )
    if existing_email.scalar():
        raise ValueError("该邮箱已被注册")
    
    # 生成验证码
    code = generate_verification_code()
    
    # 将验证码存储到 Redis，5分钟过期
    redis_client = await get_redis()
    cache_key = f"verification_code:{email}"
    await redis_client.set(cache_key, code, expire=300)
    
    # 发送验证码邮件
    await send_email(email, code)


async def register_service(user_data, db: AsyncSession):
    """注册服务
    
    Args:
        user_data: 用户注册数据
        db: 数据库会话
    
    Returns:
        User: 新创建的用户
    
    Raises:
        ValueError: 验证码错误或已过期，用户名或邮箱已存在
    """
    # 验证邮箱验证码
    redis_client = await get_redis()
    cache_key = f"verification_code:{user_data.email}"
    cached_code = await redis_client.get(cache_key)
    
    if not cached_code:
        raise ValueError("验证码已过期或不存在")
    
    if cached_code.decode() != user_data.code:
        raise ValueError("验证码错误")
    
    # 检查用户名是否已存在
    existing_user = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_user.scalar():
        raise ValueError("用户名已存在")
    
    # 检查邮箱是否已存在
    existing_email = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_email.scalar():
        raise ValueError("邮箱已被注册")
    
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


async def login_service(email: str, password: str, db: AsyncSession):
    """登录服务
    
    Args:
        email: 邮箱地址
        password: 密码
        db: 数据库会话
    
    Returns:
        tuple: (用户, token)
    
    Raises:
        ValueError: 邮箱或密码错误，账号已被禁用
    """
    # 查找用户
    result = await db.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar()
    
    # 验证用户是否存在
    if not user:
        raise ValueError("邮箱或密码错误")
    
    # 验证用户是否激活
    if not user.is_active:
        raise ValueError("账号已被禁用")
    
    # 验证密码
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise ValueError("邮箱或密码错误")
    
    # 创建访问令牌
    from datetime import timedelta
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return user, access_token
