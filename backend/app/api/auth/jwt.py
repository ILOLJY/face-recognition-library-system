"""JWT 处理模块"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

# JWT 配置
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 开发环境下使用默认密钥（生产环境必须设置环境变量）
if not SECRET_KEY:
    if os.getenv("ENVIRONMENT") != "production":
        SECRET_KEY = "your-secret-key-here-for-development-only"
        print("WARNING: Using default SECRET_KEY for development. Set SECRET_KEY environment variable for production.")
    else:
        raise ValueError("SECRET_KEY must be set in production environment")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间
    
    Returns:
        str: JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """验证令牌
    
    Args:
        token: JWT token
    
    Returns:
        dict: 解码后的数据
    
    Raises:
        JWTError: 令牌无效或已过期
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e
