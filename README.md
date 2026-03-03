# 基于人脸识别的图书借阅系统

一个利用人脸识别技术实现图书借阅管理的系统。

## 技术栈

- **后端**: FastAPI + Python 3.11
- **数据库**: PostgreSQL + SQLAlchemy 2.x
- **缓存**: Redis
- **服务器**: Uvicorn

## 项目结构

```
├── backend/
│   ├── app/
│   │   ├── db/              # 数据库模块
│   │   │   ├── base.py      # SQLAlchemy 基类
│   │   │   └── session.py   # 数据库会话管理
│   │   ├── models/          # 数据模型
│   │   │   └── users.py     # 用户模型
│   │   └── main.py          # 应用入口
│   ├── requirements.txt     # 依赖列表
│   └── test_main.http       # API 测试文件
├── .gitignore
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置数据库

在 `app/db/session.py` 中配置 PostgreSQL 数据库连接：

```python
SQLALCHEMY_DATABASE_URL = "postgresql://用户名:密码@localhost:5432/数据库名"
```

### 3. 启动服务

```bash
cd backend
uvicorn app.main:app --reload
```

服务启动后访问 http://127.0.0.1:8000

### 4. API 文档

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 功能特性

- [ ] 用户注册与登录
- [ ] 人脸识别身份验证
- [ ] 图书借阅管理
- [ ] 图书归还管理
- [ ] 借阅记录查询
- [ ] 管理员功能

## 开发说明

- 数据库模型定义在 `app/models/` 目录下
- 数据库连接配置在 `app/db/session.py` 中
- API 路由在 `app/main.py` 中定义
