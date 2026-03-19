from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import sys

from app.db.session import engine
from app.db.base import Base
from app.api.router import api_router
from app.cache.redis import redis_client

# ================= 日志配置（关键） =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # ⭐ 强制输出到控制台
    ],
    force=True  # ⭐ 覆盖 uvicorn 默认日志配置
)

logger = logging.getLogger("app")

# ================= 中间件 =================
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"➡️ 请求: {request.method} {request.url}")

        response = await call_next(request)

        logger.info(f"⬅️ 响应状态: {response.status_code}")
        return response


# ================= 创建应用 =================
app = FastAPI(
    title="图书借阅系统 API",
    description="基于人脸识别的图书借阅系统",
    version="1.0.0"
)

# ⭐ 一定要在最前面注册
app.add_middleware(LogMiddleware)

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= 路由 =================
app.include_router(api_router, prefix="/api")


# ================= 生命周期 =================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await redis_client.connect()
    logger.info("✅ Redis 连接成功")


@app.on_event("shutdown")
async def shutdown():
    await redis_client.close()
    logger.info("✅ Redis 连接关闭")


# ================= 测试接口 =================
@app.get("/")
async def root():
    return {"message": "Library System Running"}

