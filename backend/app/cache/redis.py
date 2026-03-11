import redis.asyncio as redis
from typing import Optional, Any
import json


class RedisClient:
    """Redis 客户端"""
    
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0, password: Optional[str] = None):
        """初始化 Redis 客户端
        
        Args:
            host: Redis 服务器地址
            port: Redis 服务器端口
            db: 数据库编号
            password: 密码
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.redis: Optional[redis.Redis] = None
    
    async def connect(self):
        """连接 Redis"""
        self.redis = await redis.from_url(
            f"redis://{self.host}:{self.port}/{self.db}",
            password=self.password,
            encoding="utf-8",
            decode_responses=True
        )
        return self.redis
    
    async def close(self):
        """关闭连接"""
        if self.redis:
            await self.redis.close()
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """设置键值对
        
        Args:
            key: 键
            value: 值
            expire: 过期时间（秒）
            
        Returns:
            bool: 是否成功
        """
        if not self.redis:
            await self.connect()
        
        # 序列化值
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        result = await self.redis.set(key, value)
        
        if expire:
            await self.redis.expire(key, expire)
        
        return result
    
    async def get(self, key: str) -> Optional[Any]:
        """获取值
        
        Args:
            key: 键
            
        Returns:
            Any: 值
        """
        if not self.redis:
            await self.connect()
        
        value = await self.redis.get(key)
        
        if value:
            # 尝试反序列化 JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        
        return None
    
    async def delete(self, key: str) -> int:
        """删除键
        
        Args:
            key: 键
            
        Returns:
            int: 受影响的键数
        """
        if not self.redis:
            await self.connect()
        
        return await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """检查键是否存在
        
        Args:
            key: 键
            
        Returns:
            bool: 是否存在
        """
        if not self.redis:
            await self.connect()
        
        return bool(await self.redis.exists(key))
    
    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间
        
        Args:
            key: 键
            seconds: 过期时间（秒）
            
        Returns:
            bool: 是否成功
        """
        if not self.redis:
            await self.connect()
        
        return await self.redis.expire(key, seconds)
    
    async def ttl(self, key: str) -> int:
        """获取剩余过期时间
        
        Args:
            key: 键
            
        Returns:
            int: 剩余时间（秒）
        """
        if not self.redis:
            await self.connect()
        
        return await self.redis.ttl(key)


# 全局 Redis 客户端实例
redis_client = RedisClient()


async def get_redis():
    """获取 Redis 客户端
    
    Returns:
        RedisClient: Redis 客户端
    """
    if not redis_client.redis:
        await redis_client.connect()
    return redis_client
