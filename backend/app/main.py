from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router
from app.cache.redis import redis_client

app = FastAPI(
    title="图书借阅系统 API",
    description="基于人脸识别的图书借阅系统",
    version="1.0.0"
)

# 包含 API 路由
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 连接 Redis
    await redis_client.connect()
    print("✅ Redis 连接成功")

@app.on_event("shutdown")
async def shutdown():
    # 关闭 Redis 连接
    await redis_client.close()
    print("✅ Redis 连接关闭")

@app.get("/")
async def root():
    return {"message": "Library System Running"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
