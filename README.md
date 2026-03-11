# 基于人脸识别的图书借阅系统

一个利用人脸识别技术实现图书借阅管理的系统。

## 技术栈

- **后端**: FastAPI + Python 3.11
- **数据库**: PostgreSQL + SQLAlchemy 2.x
- **缓存**: Redis
- **服务器**: Uvicorn
- **数据库迁移**: Alembic

## 项目结构

```
├── backend/
│   ├── alembic/                   # 数据库迁移目录
│   │   ├── versions/              # 迁移脚本
│   │   ├── env.py                 # 迁移环境配置
│   │   └── script.py.mako         # 迁移脚本模板
│   ├── app/
│   │   ├── cache/                 # 缓存模块
│   │   │   ├── __init__.py
│   │   │   └── redis.py           # Redis 连接管理
│   │   ├── db/                    # 数据库模块
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # SQLAlchemy 基类
│   │   │   └── session.py         # 数据库会话管理
│   │   ├── models/                # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── users.py           # 用户模型（管理员/普通用户）
│   │   │   ├── face_data.py       # 人脸特征模型
│   │   │   ├── books.py           # 图书模型
│   │   │   └── borrow_records.py  # 借阅记录模型
│   │   ├── __init__.py
│   │   └── main.py                # 应用入口
│   ├── alembic.ini                # Alembic 配置文件
│   ├── requirements.txt           # 依赖列表
│   └── test_main.http             # API 测试文件
├── .gitignore
└── README.md
```

## 核心功能

- **用户管理**：注册、登录、权限控制（管理员/普通用户）
- **人脸识别**：身份核验、人脸特征存储与匹配
- **图书管理**：图书信息维护、分类管理、库存管理
- **借阅管理**：借阅登记、归还核验、续借功能
- **逾期提醒**：自动检测逾期记录并发送提醒
- **统计分析**：借阅数据统计、热门图书分析

## 数据模型

### 1. 用户模型 (users.py)
- **角色区分**: 管理员(admin) / 普通用户(user)
- **字段**: 用户名、密码、邮箱、头像、角色、状态、创建/更新时间
- **关系**: 一个用户对应一个人脸特征，一个用户有多条借阅记录

### 2. 人脸特征模型 (face_data.py)
- **用途**: 存储用户的人脸识别数据
- **字段**: 用户ID（外键）、人脸特征向量、人脸照片路径、创建/更新时间
- **关系**: 一对一关联用户表，级联删除

### 3. 图书模型 (books.py)
- **状态**: 可借阅(available)、已借出(borrowed)、已预约(reserved)、损坏(damaged)、丢失(lost)
- **字段**: ISBN、书名、作者、出版社、出版日期、分类、简介、封面、库存数量、存放位置、状态
- **关系**: 一本书有多条借阅记录

### 4. 借阅记录模型 (borrow_records.py)
- **状态**: 借阅中(borrowed)、已归还(returned)、逾期(overdue)、已续借(renewed)
- **字段**: 用户ID、图书ID（外键）、借阅日期、应还日期、实际归还日期、状态、续借次数、罚款金额、备注
- **关系**: 关联用户表和图书表

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库

在 `app/db/session.py` 中配置 PostgreSQL 数据库连接：

```python
DATABASE_URL = "postgresql+asyncpg://postgres:151004@localhost:5432/library_db"
```

### 3. 数据库迁移

```bash
# 创建初始迁移
cd backend
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
cd backend
alembic upgrade head

# 查看迁移状态
cd backend
alembic current
```

### 4. 启动服务

```bash
cd backend
uvicorn app.main:app --reload
```

服务启动后访问 http://127.0.0.1:8000

### 5. API 文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 系统特性

- **双角色设计**：管理员与读者分离，权限明确
- **人脸识别**：集成人脸识别 SDK 实现身份核验
- **高效流程**：借阅登记、归还核验、逾期提醒全流程自动化
- **数据安全**：密码加密存储，敏感数据保护
- **系统稳定**：支持并发，响应延迟低
- **可扩展性**：模块化设计，易于功能扩展
- **缓存机制**：使用 Redis 缓存提升性能

## 开发说明

- 数据库模型定义在 `app/models/` 目录下
- 数据库连接配置在 `app/db/session.py` 中
- 数据库迁移配置在 `alembic/` 目录下
- Redis 缓存配置在 `app/cache/redis.py` 中（默认端口 6379）
- API 路由在 `app/main.py` 中定义
- 所有模型字段均带有详细的中文注释

## Redis 缓存使用

### 配置
- 默认连接：localhost:6379，db=0
- 可在 `RedisClient` 初始化时修改配置

### 使用示例

```python
from app.cache.redis import get_redis

# 获取 Redis 客户端
redis_client = await get_redis()

# 存储数据
await redis_client.set("user:123", {"name": "张三", "role": "user"})

# 获取数据
user_data = await redis_client.get("user:123")

# 设置过期时间
await redis_client.set("token:123", "abc123", expire=3600)
```

## 数据库关系图

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    users    │       │  face_data  │       │    books    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────┤ user_id(FK) │       │ id (PK)     │
│ username    │   1:1 │face_encoding│       │ isbn        │
│ password    │       │ face_image  │       │ title       │
│ email       │       └─────────────┘       │ author      │
│ avatar      │                             │ ...         │
│ role        │                             └──────┬──────┘
│ ...         │                                    │
└──────┬──────┘                                    │
       │                                           │
       │ 1:N                                       │ 1:N
       │                                           │
       ▼                                           ▼
┌─────────────┐
│borrow_records│
├─────────────┤
│ id (PK)     │
│ user_id(FK) │
│ book_id(FK) │
│ borrow_date │
│ due_date    │
│ status      │
│ ...         │
└─────────────┘
```

## 项目状态

- ✅ 数据库模型设计完成
- ✅ 数据库迁移配置完成
- ✅ Redis 缓存模块完成
- ✅ 基本项目结构搭建
- 🔄 核心功能开发中
- 🔄 人脸识别集成中
