# 基于人脸识别的图书借阅系统

一个利用人脸识别技术实现图书借阅管理的系统。

## 前端环境

- **框架**: Vue 3 + JavaScript
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **UI 框架**: Element Plus
- **网络请求**: Axios

## 前端项目结构

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── assets/         # 资源文件
│   ├── components/     # 组件
│   ├── router/         # 路由配置
│   │   ├── views/          # 视图页面
│   │   │   ├── HomeView.vue       # 首页
│   │   │   ├── LoginView.vue      # 登录页
│   │   │   ├── RegisterView.vue   # 注册页
│   │   │   ├── BooksView.vue      # 图书列表
│   │   │   ├── BookDetailView.vue # 图书详情
│   │   │   ├── BorrowView.vue     # 借阅记录
│   │   │   ├── ProfileView.vue    # 个人中心
│   │   │   ├── ReadmeView.vue     # 系统文档
│   │   │   ├── AdminLoginView.vue # 管理员登录页
│   │   │   └── AdminView.vue      # 管理员页面
│   ├── App.vue         # 应用入口
│   ├── main.js         # 主文件
│   └── style.css       # 全局样式
├── .gitignore
├── package.json        # 项目配置
└── vite.config.js      # Vite 配置
```

## 前端快速开始

### 1. 安装依赖

```bash
cd frontend
npm install
```

### 2. 启动开发服务器

```bash
cd frontend
npm run dev
```

服务启动后访问 http://localhost:5173/

### 3. 构建生产版本

```bash
cd frontend
npm run build
```

构建后的文件会生成在 `dist` 目录中。

---



## 技术栈

- **后端**: FastAPI + Python 3.11
- **数据库**: PostgreSQL + SQLAlchemy 2.x
- **缓存**: Redis
- **服务器**: Uvicorn
- **数据库迁移**: Alembic
- **密码加密**: bcrypt
- **邮箱验证**: email-validator

## 项目结构

```
├── backend/
│   ├── alembic/                   # 数据库迁移目录
│   │   ├── versions/              # 迁移脚本
│   │   ├── env.py                 # 迁移环境配置
│   │   └── script.py.mako         # 迁移脚本模板
│   ├── app/
│   │   ├── api/                   # API 接口模块
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # API 路由管理
│   │   │   └── auth/              # 认证模块
│   │   │       ├── __init__.py
│   │   │       ├── router.py      # 认证路由
│   │   │       ├── service.py     # 业务逻辑
│   │   │       ├── jwt.py         # JWT 处理
│   │   │       └── dependencies.py # 依赖函数
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
- **邮箱验证**：注册时发送验证码，5分钟有效期
- **人脸识别**：身份核验、人脸特征存储与匹配
- **图书管理**：图书信息维护、分类管理、库存管理
- **借阅管理**：借阅登记、归还核验、续借功能
- **逾期提醒**：自动检测逾期记录并发送提醒
- **统计分析**：借阅数据统计、热门图书分析
- **最近借阅**：基于Redis List实现最近借阅图书列表，新借阅的图书放在最上面
- **图书搜索**：支持按标题、作者、出版社搜索图书

## API 接口

### 认证接口

#### 1. 发送注册验证码
- **接口**: `POST /api/auth/send-code/register`
- **描述**: 向指定邮箱发送6位数字验证码（用于注册）
- **请求参数**:
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **响应**:
  ```json
  {
    "message": "验证码已发送到您的邮箱"
  }
  ```

#### 2. 用户注册
- **接口**: `POST /api/auth/register`
- **描述**: 完成用户注册（需要邮箱验证码）
- **请求参数**:
  ```json
  {
    "username": "testuser",
    "password": "123456",
    "email": "user@example.com",
    "code": "123456",
    "avatar": "",
    "role": "USER"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "avatar": "",
    "role": "USER",
    "is_active": true
  }
  ```

#### 3. 用户登录
- **接口**: `POST /api/auth/login`
- **描述**: 用户登录（使用邮箱和密码）
- **请求参数**:
  ```json
  {
    "email": "user@example.com",
    "password": "123456"
  }
  ```
- **响应**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "user@example.com",
      "avatar": "",
      "role": "USER",
      "is_active": true
    }
  }
  ```

#### 4. 获取当前用户信息
- **接口**: `GET /api/auth/me`
- **描述**: 获取当前登录用户的信息（需要在请求头中携带 Authorization: Bearer <token>）
- **请求头**:
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "avatar": "",
    "role": "USER",
    "is_active": true
  }
  ```

#### 5. 获取当前用户ID
- **接口**: `GET /api/auth/me/id`
- **描述**: 获取当前登录用户的ID（需要在请求头中携带 Authorization: Bearer <token>）
- **请求头**:
  ```
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
- **响应**:
  ```json
  {
    "user_id": 1
  }
  ```

#### 6. 用户登出
- **接口**: `POST /api/auth/logout`
- **描述**: 用户登出，删除 HttpOnly cookie 中的 token
- **请求参数**: 无
- **响应**:
  ```json
  {
    "msg": "退出成功"
  }
  ```

### 用户接口

#### 1. 获取用户个人信息
- **接口**: `GET /api/users/profile`
- **描述**: 获取当前登录用户的详细信息
- **响应**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "avatar": "/static/avatars/1_1234567890.jpg",
    "role": "user",
    "is_active": true,
    "created_at": "2026-03-18T00:00:00"
  }
  ```

#### 2. 修改用户名
- **接口**: `PUT /api/users/profile/username`
- **描述**: 修改当前用户的用户名
- **请求参数**:
  ```json
  {
    "username": "newusername"
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "username": "newusername",
    "email": "user@example.com",
    "avatar": "/static/avatars/1_1234567890.jpg",
    "role": "user",
    "is_active": true,
    "created_at": "2026-03-18T00:00:00"
  }
  ```

#### 3. 修改密码
- **接口**: `PUT /api/users/profile/password`
- **描述**: 修改当前用户的密码
- **请求参数**:
  ```json
  {
    "old_password": "oldpassword",
    "new_password": "newpassword"
  }
  ```
- **响应**:
  ```json
  {
    "msg": "密码修改成功"
  }
  ```

#### 4. 上传头像
- **接口**: `POST /api/users/profile/avatar`
- **描述**: 上传用户头像
- **请求参数**: 表单数据，字段名为 `file`，类型为文件
- **响应**:
  ```json
  {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "avatar": "/static/avatars/1_1234567890.jpg",
    "role": "user",
    "is_active": true,
    "created_at": "2026-03-18T00:00:00"
  }
  ```

### 管理员接口

#### 1. 管理员登录
- **接口**: `POST /api/auth/admin/login`
- **描述**: 管理员登录，验证用户密码和管理员权限
- **请求参数**:
  ```json
  {
    "email": "admin@example.com",
    "password": "adminpassword"
  }
  ```
- **响应**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "avatar": "",
      "role": "admin",
      "is_active": true
    }
  }
  ```

#### 2. 获取所有图书
- **接口**: `GET /api/admin/books`
- **描述**: 获取所有图书信息（仅管理员可访问）
- **响应**:
  ```json
  [
    {
      "id": 1,
      "title": "Python 编程从入门到实践",
      "author": "Eric Matthes",
      "isbn": "9787115428028",
      "publisher": "人民邮电出版社",
      "publish_date": "2016-07-01",
      "category": "计算机",
      "description": "Python入门经典图书",
      "cover_image": "/static/covers/1_book.jpg",
      "total_copies": 5,
      "available_copies": 3,
      "location": "A区1层",
      "status": "available",
      "created_at": "2026-03-18T00:00:00",
      "updated_at": "2026-03-18T00:00:00"
    }
  ]
  ```

#### 3. 添加图书
- **接口**: `POST /api/admin/books`
- **描述**: 添加新图书（仅管理员可访问）
- **请求参数**:
  ```json
  {
    "title": "深入理解计算机系统",
    "author": "Randal E. Bryant",
    "isbn": "9787111407010",
    "publisher": "机械工业出版社",
    "publish_date": "2016-01-01",
    "category": "计算机",
    "description": "深入理解计算机系统原理",
    "total_copies": 3,
    "available_copies": 3,
    "location": "A区2层"
  }
  ```
- **响应**:
  ```json
  {
    "id": 2,
    "title": "深入理解计算机系统",
    "author": "Randal E. Bryant",
    "isbn": "9787111407010",
    "publisher": "机械工业出版社",
    "publish_date": "2016-01-01",
    "category": "计算机",
    "description": "深入理解计算机系统原理",
    "cover_image": null,
    "total_copies": 3,
    "available_copies": 3,
    "location": "A区2层",
    "status": "available",
    "created_at": "2026-03-24T00:00:00",
    "updated_at": "2026-03-24T00:00:00"
  }
  ```

#### 4. 编辑图书
- **接口**: `PUT /api/admin/books/{book_id}`
- **描述**: 编辑图书信息（仅管理员可访问）
- **请求参数**:
  ```json
  {
    "title": "深入理解计算机系统（第3版）",
    "total_copies": 5,
    "available_copies": 5
  }
  ```
- **响应**:
  ```json
  {
    "id": 2,
    "title": "深入理解计算机系统（第3版）",
    "author": "Randal E. Bryant",
    "isbn": "9787111407010",
    "publisher": "机械工业出版社",
    "publish_date": "2016-01-01",
    "category": "计算机",
    "description": "深入理解计算机系统原理",
    "cover_image": null,
    "total_copies": 5,
    "available_copies": 5,
    "location": "A区2层",
    "status": "available",
    "created_at": "2026-03-24T00:00:00",
    "updated_at": "2026-03-24T00:00:00"
  }
  ```

#### 5. 删除图书
- **接口**: `DELETE /api/admin/books/{book_id}`
- **描述**: 删除图书（仅管理员可访问）
- **响应**:
  ```json
  {
    "msg": "图书删除成功"
  }
  ```

#### 6. 上传图书封面
- **接口**: `POST /api/admin/books/{book_id}/cover`
- **描述**: 上传图书封面（仅管理员可访问）
- **请求参数**: 表单数据，字段名为 `file`，类型为文件
- **响应**:
  ```json
  {
    "id": 2,
    "title": "深入理解计算机系统（第3版）",
    "author": "Randal E. Bryant",
    "isbn": "9787111407010",
    "publisher": "机械工业出版社",
    "publish_date": "2016-01-01",
    "category": "计算机",
    "description": "深入理解计算机系统原理",
    "cover_image": "/static/covers/2_book.jpg",
    "total_copies": 5,
    "available_copies": 5,
    "location": "A区2层",
    "status": "available",
    "created_at": "2026-03-24T00:00:00",
    "updated_at": "2026-03-24T00:00:00"
  }
  ```

### 图书接口

#### 1. 获取最近借阅的图书
- **接口**: `GET /api/books/recent`
- **描述**: 获取最近借阅的图书（最多10本），Redis 实时维护，新借阅的图书放在最上面
- **响应**:
  ```json
  [
    {
      "id": 2,
      "title": "深入理解计算机系统",
      "author": "Randal E. Bryant",
      "publisher": "机械工业出版社",
      "cover_image": "/static/covers/2_book.jpg"
    }
  ]
  ```

#### 2. 获取图书详情
- **接口**: `GET /api/books/{book_id}`
- **描述**: 获取指定图书的详细信息
- **响应**:
  ```json
  {
    "id": 1,
    "title": "Python 编程从入门到实践",
    "author": "Eric Matthes",
    "isbn": "9787115428028",
    "publisher": "人民邮电出版社",
    "publish_date": "2016-07-01",
    "category": "计算机",
    "description": "Python入门经典图书",
    "cover_image": "/static/covers/1_book.jpg",
    "total_copies": 5,
    "available_copies": 3,
    "location": "A区1层",
    "status": "available",
    "created_at": "2026-03-18T00:00:00",
    "updated_at": "2026-03-18T00:00:00"
  }
  ```

#### 3. 搜索图书
- **接口**: `GET /api/books/search?keyword=Python`
- **描述**: 根据关键词搜索图书，支持搜索标题、作者、出版社、分类和描述
- **响应**:
  ```json
  [
    {
      "id": 1,
      "title": "Python 编程从入门到实践",
      "author": "Eric Matthes",
      "publisher": "人民邮电出版社",
      "cover_image": "/static/covers/1_book.jpg"
    }
  ]
  ```

### 借阅接口

#### 1. 借阅图书
- **接口**: `POST /api/borrow/borrow`
- **描述**: 借阅图书
- **请求参数**:
  ```json
  {
    "book_id": 1
  }
  ```
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "book_id": 1,
    "borrow_date": "2026-03-24T00:00:00",
    "due_date": "2026-04-07T00:00:00",
    "return_date": null,
    "status": "borrowed",
    "renew_count": 0,
    "fine_amount": 0.0,
    "created_at": "2026-03-24T00:00:00",
    "updated_at": "2026-03-24T00:00:00"
  }
  ```

#### 2. 归还图书
- **接口**: `POST /api/borrow/return/{record_id}`
- **描述**: 归还图书
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "book_id": 1,
    "borrow_date": "2026-03-24T00:00:00",
    "due_date": "2026-04-07T00:00:00",
    "return_date": "2026-04-01T00:00:00",
    "status": "returned",
    "renew_count": 0,
    "fine_amount": 0.0,
    "created_at": "2026-03-24T00:00:00",
    "updated_at": "2026-04-01T00:00:00"
  }
  ```

#### 3. 获取用户借阅记录
- **接口**: `GET /api/borrow/records`
- **描述**: 获取当前用户的借阅记录
- **响应**:
  ```json
  [
    {
      "id": 1,
      "user_id": 1,
      "book_id": 1,
      "borrow_date": "2026-03-24T00:00:00",
      "due_date": "2026-04-07T00:00:00",
      "return_date": null,
      "status": "borrowed",
      "renew_count": 0,
      "fine_amount": 0.0,
      "created_at": "2026-03-24T00:00:00",
      "updated_at": "2026-03-24T00:00:00"
    }
  ]
  ```

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

### 3. 配置环境变量

创建 `.env` 文件或设置系统环境变量：

```
# 数据库连接
DATABASE_URL="postgresql+asyncpg://postgres:151004@localhost:5432/library_db"

# JWT 密钥（生产环境必须设置）
SECRET_KEY="your-secret-key-here"

# 邮箱配置（生产环境必须设置）
EMAIL_PASSWORD="your_163_email_authorization_code"

# 环境模式
ENVIRONMENT="development"  # 可选：development, production
```

注意：
- 163邮箱需要开启 SMTP 服务并获取授权码
- 465端口需要使用 SSL 连接
- 生产环境必须设置 SECRET_KEY 和 EMAIL_PASSWORD

### 4. 数据库迁移

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

### 5. 启动服务

```bash
cd backend
uvicorn app.main:app --reload
```

服务启动后访问 http://127.0.0.1:8000

### 6. API 文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 系统特性

- **双角色设计**：管理员与读者分离，权限明确
- **邮箱验证**：注册时验证码验证，5分钟有效期
- **人脸识别**：集成人脸识别 SDK 实现身份核验
- **高效流程**：借阅登记、归还核验、逾期提醒全流程自动化
- **数据安全**：密码加密存储，敏感数据保护
- **系统稳定**：支持并发，响应延迟低
- **可扩展性**：模块化设计，易于功能扩展
- **缓存机制**：使用 Redis 缓存提升性能
- **安全认证**：使用 HttpOnly cookie 存储 JWT token，防止 XSS 攻击
- **路由守卫**：前端路由守卫，未登录用户自动跳转到登录页面
- **注销功能**：支持用户注销登录，后端删除 HttpOnly cookie
- **接口封装**：前端统一封装 API 接口，便于维护
- **完整认证流程**：登录 → 存储 token → 请求验证 → 注销

## 开发说明

- 数据库模型定义在 `app/models/` 目录下
- 数据库连接配置在 `app/db/session.py` 中
- 数据库迁移配置在 `alembic/` 目录下
- Redis 缓存配置在 `app/cache/redis.py` 中（默认端口 6379）
- API 接口定义在 `app/api/` 目录下
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
- ✅ 用户注册接口完成（两步注册流程）
- ✅ 邮箱验证码功能完成
- ✅ 登录接口完成（JWT 鉴权）
- ✅ JWT 令牌验证完成
- ✅ 基本项目结构搭建
- ✅ 前端路由守卫完成
- ✅ 后端鉴权机制完成
- ✅ 管理员登录和管理页面完成
- ✅ 图书管理功能完成
- ✅ 借阅管理功能完成
- ✅ 最近借阅图书列表功能完成
- ✅ 图书搜索功能完成
- ✅ 前端API接口封装完成
- 🔄 人脸识别集成中
