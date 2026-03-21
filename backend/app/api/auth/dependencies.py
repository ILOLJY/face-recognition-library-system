"""认证依赖模块"""
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.users import User
from app.api.auth.jwt import verify_token


async def get_current_user(
    access_token: str = Cookie(...),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户
    
    Args:
        access_token: 从 cookie 中获取的 token
        db: 数据库会话
    
    Returns:
        User: 当前用户
    
    Raises:
        HTTPException: 认证失败
    """
    try:
        payload = verify_token(access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
        )
    
    user_id = int(payload.get("sub"))
    
    # 从数据库获取用户
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return user


async def get_current_user_id(
    access_token: str = Cookie(...)
) -> int:
    """获取当前用户ID
    
    Args:
        access_token: 从 cookie 中获取的 token
    
    Returns:
        int: 用户ID
    
    Raises:
        HTTPException: 认证失败
    """
    try:
        payload = verify_token(access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
        )
    
    return int(payload.get("sub"))
