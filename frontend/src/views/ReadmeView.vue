<template>
  <div class="readme">
    <el-container>
      <el-main>
        <div class="readme-header">
          <el-button type="default" @click="router.push('/home')" style="margin-bottom: 20px;">
            <el-icon><ArrowLeft /></el-icon>
            返回主页
          </el-button>
          <h1>基于人脸识别的图书借阅系统</h1>
          <p class="subtitle">系统使用文档</p>
        </div>
        
        <div class="readme-content">
          <!-- 左侧导航 -->
          <div class="readme-sidebar">
            <el-menu
              default-active="1"
              class="readme-menu"
              @select="handleMenuSelect"
            >
              <el-menu-item index="1">
                <el-icon><House /></el-icon>
                <span>系统简介</span>
              </el-menu-item>
              <el-menu-item index="2">
                <el-icon><Operation /></el-icon>
                <span>系统功能</span>
              </el-menu-item>
              <el-menu-item index="3">
                <el-icon><Timer /></el-icon>
                <span>认证流程</span>
              </el-menu-item>
              <el-menu-item index="4">
                <el-icon><Bell /></el-icon>
                <span>API 接口</span>
                <el-menu>
                  <el-menu-item index="4-1">
                    <span>认证接口</span>
                  </el-menu-item>
                  <el-menu-item index="4-2">
                    <span>用户接口</span>
                  </el-menu-item>
                  <el-menu-item index="4-3">
                    <span>管理员接口</span>
                  </el-menu-item>
                </el-menu>
              </el-menu-item>
              <el-menu-item index="5">
                <el-icon><Cpu /></el-icon>
                <span>技术栈</span>
              </el-menu-item>

              <el-menu-item index="6">
                <el-icon><DataAnalysis /></el-icon>
                <span>数据模型</span>
              </el-menu-item>
              <el-menu-item index="7">
                <el-icon><Guide /></el-icon>
                <span>快速开始</span>
                <el-menu>
                  <el-menu-item index="7-1">
                    <span>前端快速开始</span>
                  </el-menu-item>
                  <el-menu-item index="7-2">
                    <span>后端快速开始</span>
                  </el-menu-item>
                </el-menu>
              </el-menu-item>
              <el-menu-item index="8">
                <el-icon><Star /></el-icon>
                <span>系统特性</span>
              </el-menu-item>
              <el-menu-item index="9">
                <el-icon><Document /></el-icon>
                <span>开发说明</span>
              </el-menu-item>
              <el-menu-item index="10">
                <el-icon><Setting /></el-icon>
                <span>Redis缓存</span>
              </el-menu-item>
              <el-menu-item index="11">
                <el-icon><Link /></el-icon>
                <span>数据库关系</span>
              </el-menu-item>
              <el-menu-item index="12">
                <el-icon><Timer /></el-icon>
                <span>项目状态</span>
              </el-menu-item>
            </el-menu>
          </div>
          
          <!-- 右侧内容 -->
          <div class="readme-main">
            <div id="intro" class="readme-section">
              <h2>系统简介</h2>
              <p>基于人脸识别的图书借阅系统是一个现代化的图书馆管理系统，利用人脸识别技术实现身份核验，提高借阅效率和安全性。系统支持管理员和读者双角色，提供图书信息管理、借阅登记、归还核验、逾期提醒等核心功能。</p>
              <h3>系统特点</h3>
              <ul>
                <li>人脸识别身份核验，提升安全性</li>
                <li>双角色设计，满足管理员和读者需求</li>
                <li>响应式设计，适配各种设备</li>
                <li>高效的借阅流程，减少人工操作</li>
                <li>完善的权限控制，保障系统安全</li>
              </ul>
            </div>
            
            <div id="features" class="readme-section">
              <h2>系统功能</h2>
              <h3>读者功能</h3>
              <ul>
                <li>用户注册与登录</li>
                <li>个人信息管理</li>
                <li>图书查询与借阅</li>
                <li>借阅记录查询</li>
                <li>人脸信息管理</li>
              </ul>
              <h3>管理员功能</h3>
              <ul>
                <li>图书信息管理（添加、编辑、删除）</li>
                <li>借阅记录管理</li>
                <li>用户管理</li>
                <li>系统设置</li>
              </ul>
            </div>
            
            <div id="auth-flow" class="readme-section">
              <h2>认证流程</h2>
              <ol>
                <li>用户注册：填写个人信息，获取邮箱验证码，完成注册</li>
                <li>用户登录：输入邮箱和密码，系统验证身份</li>
                <li>身份核验：使用人脸识别技术验证用户身份</li>
                <li>权限控制：根据用户角色提供不同的功能访问权限</li>
              </ol>
            </div>
            
            <div id="api" class="readme-section">
              <h2>API 接口</h2>
              
              <div id="auth-api" class="api-subsection">
                <h3>认证接口</h3>
                <table class="api-table">
                  <thead>
                    <tr>
                      <th>接口</th>
                      <th>方法</th>
                      <th>描述</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>/api/auth/send-code/register</td>
                      <td>POST</td>
                      <td>发送注册验证码</td>
                    </tr>
                    <tr>
                      <td>/api/auth/register</td>
                      <td>POST</td>
                      <td>用户注册</td>
                    </tr>
                    <tr>
                      <td>/api/auth/login</td>
                      <td>POST</td>
                      <td>用户登录</td>
                    </tr>
                    <tr>
                      <td>/api/auth/admin/login</td>
                      <td>POST</td>
                      <td>管理员登录</td>
                    </tr>
                    <tr>
                      <td>/api/auth/me</td>
                      <td>GET</td>
                      <td>获取当前用户信息</td>
                    </tr>
                    <tr>
                      <td>/api/auth/logout</td>
                      <td>POST</td>
                      <td>用户注销</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div id="user-api" class="api-subsection">
                <h3>用户接口</h3>
                <table class="api-table">
                  <thead>
                    <tr>
                      <th>接口</th>
                      <th>方法</th>
                      <th>描述</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>/api/users/profile</td>
                      <td>GET</td>
                      <td>获取用户个人信息</td>
                    </tr>
                    <tr>
                      <td>/api/users/profile/username</td>
                      <td>PUT</td>
                      <td>修改用户名</td>
                    </tr>
                    <tr>
                      <td>/api/users/profile/password</td>
                      <td>PUT</td>
                      <td>修改密码</td>
                    </tr>
                    <tr>
                      <td>/api/users/profile/avatar</td>
                      <td>POST</td>
                      <td>上传头像</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div id="admin-api" class="api-subsection">
                <h3>管理员接口</h3>
                <table class="api-table">
                  <thead>
                    <tr>
                      <th>接口</th>
                      <th>方法</th>
                      <th>描述</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>/api/admin/books</td>
                      <td>GET</td>
                      <td>获取所有图书</td>
                    </tr>
                    <tr>
                      <td>/api/admin/books</td>
                      <td>POST</td>
                      <td>添加图书</td>
                    </tr>
                    <tr>
                      <td>/api/admin/books/{book_id}</td>
                      <td>PUT</td>
                      <td>编辑图书</td>
                    </tr>
                    <tr>
                      <td>/api/admin/books/{book_id}</td>
                      <td>DELETE</td>
                      <td>删除图书</td>
                    </tr>
                    <tr>
                      <td>/api/admin/books/{book_id}/cover</td>
                      <td>POST</td>
                      <td>上传图书封面</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div id="tech-stack" class="readme-section">
              <h2>技术栈</h2>
              <h3>前端</h3>
              <ul>
                <li>Vue 3 + JavaScript</li>
                <li>Vite（构建工具）</li>
                <li>Pinia（状态管理）</li>
                <li>Vue Router 4（路由）</li>
                <li>Element Plus（UI 框架）</li>
                <li>Axios（网络请求）</li>
              </ul>
              <h3>后端</h3>
              <ul>
                <li>Python 3.11</li>
                <li>FastAPI（主框架）</li>
                <li>PostgreSQL（数据库）</li>
                <li>SQLAlchemy 2.x（ORM）</li>
                <li>Redis（缓存）</li>
                <li>Uvicorn（ASGI 服务器）</li>
                <li>Alembic（数据库迁移）</li>
                <li>bcrypt（密码加密）</li>
                <li>email-validator（邮箱验证）</li>
              </ul>
            </div>
            

            
            <div id="frontend-quickstart" class="readme-section">
              <h2>前端快速开始</h2>
              <h3>1. 安装依赖</h3>
              <pre><code>cd frontend
npm install</code></pre>
              
              <h3>2. 启动开发服务器</h3>
              <pre><code>cd frontend
npm run dev</code></pre>
              <p>服务启动后访问 http://localhost:5173/</p>
              
              <h3>3. 构建生产版本</h3>
              <pre><code>cd frontend
npm run build</code></pre>
              <p>构建后的文件会生成在 `dist` 目录中。</p>
            </div>
            
            <div id="data-models" class="readme-section">
              <h2>数据模型</h2>
              <h3>1. 用户模型 (users.py)</h3>
              <ul>
                <li><strong>角色区分</strong>: 管理员(admin) / 普通用户(user)</li>
                <li><strong>字段</strong>: 用户名、密码、邮箱、头像、角色、状态、创建/更新时间</li>
                <li><strong>关系</strong>: 一个用户对应一个人脸特征，一个用户有多条借阅记录</li>
              </ul>
              
              <h3>2. 人脸特征模型 (face_data.py)</h3>
              <ul>
                <li><strong>用途</strong>: 存储用户的人脸识别数据</li>
                <li><strong>字段</strong>: 用户ID（外键）、人脸特征向量、人脸照片路径、创建/更新时间</li>
                <li><strong>关系</strong>: 一对一关联用户表，级联删除</li>
              </ul>
              
              <h3>3. 图书模型 (books.py)</h3>
              <ul>
                <li><strong>状态</strong>: 可借阅(available)、已借出(borrowed)、已预约(reserved)、损坏(damaged)、丢失(lost)</li>
                <li><strong>字段</strong>: ISBN、书名、作者、出版社、出版日期、分类、简介、封面、库存数量、存放位置、状态</li>
                <li><strong>关系</strong>: 一本书有多条借阅记录</li>
              </ul>
              
              <h3>4. 借阅记录模型 (borrow_records.py)</h3>
              <ul>
                <li><strong>状态</strong>: 借阅中(borrowed)、已归还(returned)、逾期(overdue)、已续借(renewed)</li>
                <li><strong>字段</strong>: 用户ID、图书ID（外键）、借阅日期、应还日期、实际归还日期、状态、续借次数、罚款金额、备注</li>
                <li><strong>关系</strong>: 关联用户表和图书表</li>
              </ul>
            </div>
            
            <div id="backend-quickstart" class="readme-section">
              <h2>后端快速开始</h2>
              <h3>1. 安装依赖</h3>
              <pre><code>cd backend
pip install -r requirements.txt</code></pre>
              
              <h3>2. 配置数据库</h3>
              <p>在 `app/db/session.py` 中配置 PostgreSQL 数据库连接：</p>
              <pre><code>DATABASE_URL = "postgresql+asyncpg://postgres:151004@localhost:5432/library_db"</code></pre>
              
              <h3>3. 配置环境变量</h3>
              <p>创建 `.env` 文件或设置系统环境变量：</p>
              <pre><code># 数据库连接
DATABASE_URL="postgresql+asyncpg://postgres:151004@localhost:5432/library_db"

# JWT 密钥（生产环境必须设置）
SECRET_KEY="your-secret-key-here"

# 邮箱配置（生产环境必须设置）
EMAIL_PASSWORD="your_163_email_authorization_code"

# 环境模式
ENVIRONMENT="development"  # 可选：development, production</code></pre>
              <p>注意：</p>
              <ul>
                <li>163邮箱需要开启 SMTP 服务并获取授权码</li>
                <li>465端口需要使用 SSL 连接</li>
                <li>生产环境必须设置 SECRET_KEY 和 EMAIL_PASSWORD</li>
              </ul>
              
              <h3>4. 数据库迁移</h3>
              <pre><code># 创建初始迁移
cd backend
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
cd backend
alembic upgrade head

# 查看迁移状态
cd backend
alembic current</code></pre>
              
              <h3>5. 启动服务</h3>
              <pre><code>cd backend
uvicorn app.main:app --reload</code></pre>
              <p>服务启动后访问 http://127.0.0.1:8000</p>
              
              <h3>6. API 文档</h3>
              <ul>
                <li>Swagger UI: http://127.0.0.1:8000/docs</li>
                <li>ReDoc: http://127.0.0.1:8000/redoc</li>
              </ul>
            </div>
            
            <div id="system-features" class="readme-section">
              <h2>系统特性</h2>
              <ul>
                <li><strong>双角色设计</strong>：管理员与读者分离，权限明确</li>
                <li><strong>邮箱验证</strong>：注册时验证码验证，5分钟有效期</li>
                <li><strong>人脸识别</strong>：集成人脸识别 SDK 实现身份核验</li>
                <li><strong>高效流程</strong>：借阅登记、归还核验、逾期提醒全流程自动化</li>
                <li><strong>数据安全</strong>：密码加密存储，敏感数据保护</li>
                <li><strong>系统稳定</strong>：支持并发，响应延迟低</li>
                <li><strong>可扩展性</strong>：模块化设计，易于功能扩展</li>
                <li><strong>缓存机制</strong>：使用 Redis 缓存提升性能</li>
                <li><strong>安全认证</strong>：使用 HttpOnly cookie 存储 JWT token，防止 XSS 攻击</li>
                <li><strong>路由守卫</strong>：前端路由守卫，未登录用户自动跳转到登录页面</li>
                <li><strong>注销功能</strong>：支持用户注销登录，后端删除 HttpOnly cookie</li>
                <li><strong>接口封装</strong>：前端统一封装 API 接口，便于维护</li>
                <li><strong>完整认证流程</strong>：登录 → 存储 token → 请求验证 → 注销</li>
              </ul>
            </div>
            
            <div id="development-notes" class="readme-section">
              <h2>开发说明</h2>
              <ul>
                <li>数据库模型定义在 `app/models/` 目录下</li>
                <li>数据库连接配置在 `app/db/session.py` 中</li>
                <li>数据库迁移配置在 `alembic/` 目录下</li>
                <li>Redis 缓存配置在 `app/cache/redis.py` 中（默认端口 6379）</li>
                <li>API 接口定义在 `app/api/` 目录下</li>
                <li>API 路由在 `app/main.py` 中定义</li>
                <li>所有模型字段均带有详细的中文注释</li>
              </ul>
            </div>
            
            <div id="redis-cache" class="readme-section">
              <h2>Redis 缓存使用</h2>
              <h3>配置</h3>
              <ul>
                <li>默认连接：localhost:6379，db=0</li>
                <li>可在 `RedisClient` 初始化时修改配置</li>
              </ul>
              
              <h3>使用示例</h3>
              <pre><code>from app.cache.redis import get_redis

# 获取 Redis 客户端
redis_client = await get_redis()

# 存储数据
await redis_client.set("user:123", {"name": "张三", "role": "user"})

# 获取数据
user_data = await redis_client.get("user:123")

# 设置过期时间
await redis_client.set("token:123", "abc123", expire=3600)</code></pre>
            </div>
            
            <div id="database-relation" class="readme-section">
              <h2>数据库关系图</h2>
              <pre><code>┌─────────────┐       ┌─────────────┐       ┌─────────────┐
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
└─────────────┘</code></pre>
            </div>
            
            <div id="project-status" class="readme-section">
              <h2>项目状态</h2>
              <ul>
                <li>✅ 数据库模型设计完成</li>
                <li>✅ 数据库迁移配置完成</li>
                <li>✅ Redis 缓存模块完成</li>
                <li>✅ 用户注册接口完成（两步注册流程）</li>
                <li>✅ 邮箱验证码功能完成</li>
                <li>✅ 登录接口完成（JWT 鉴权）</li>
                <li>✅ JWT 令牌验证完成</li>
                <li>✅ 基本项目结构搭建</li>
                <li>🔄 人脸识别集成中</li>
                <li>🔄 图书管理功能开发中</li>
                <li>🔄 借阅管理功能开发中</li>
                <li>🔄 其他核心功能开发中</li>
              </ul>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ArrowLeft, House, Operation, Timer, Bell, Cpu, Files, DataAnalysis, Guide, Star, Document, Setting, Link } from '@element-plus/icons-vue'

const router = useRouter()

const handleMenuSelect = (key) => {
  console.log('菜单选择:', key)
  switch (key) {
    case '1':
      scrollToSection('intro')
      break
    case '2':
      scrollToSection('features')
      break
    case '3':
      scrollToSection('auth-flow')
      break
    case '4-1':
      scrollToSection('auth-api')
      break
    case '4-2':
      scrollToSection('user-api')
      break
    case '4-3':
      scrollToSection('admin-api')
      break
    case '5':
      scrollToSection('tech-stack')
      break
    case '6':
      scrollToSection('data-models')
      break
    case '7':
      scrollToSection('frontend-quickstart')
      break
    case '7-1':
      scrollToSection('frontend-quickstart')
      break
    case '7-2':
      scrollToSection('backend-quickstart')
      break
    case '8':
      scrollToSection('system-features')
      break
    case '9':
      scrollToSection('development-notes')
      break
    case '10':
      scrollToSection('redis-cache')
      break
    case '11':
      scrollToSection('database-relation')
      break
    case '12':
      scrollToSection('project-status')
      break
    default:
      break
  }
}

const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
.readme {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.readme-header {
  text-align: center;
  margin-bottom: 40px;
}

.readme-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 10px;
}

.readme-header .subtitle {
  font-size: 16px;
  color: #606266;
}

.readme-content {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.readme-sidebar {
  flex: 0 0 250px;
  position: sticky;
  top: 20px;
  align-self: flex-start;
}

.readme-menu {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.readme-main {
  flex: 1;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.readme-section {
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.readme-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.readme-section h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 20px;
  border-left: 4px solid #409EFF;
  padding-left: 15px;
}

.readme-section h3 {
  font-size: 18px;
  color: #409EFF;
  margin: 20px 0 15px 0;
}

.readme-section p {
  line-height: 1.6;
  color: #606266;
  margin-bottom: 15px;
}

.readme-section ul,
.readme-section ol {
  margin-left: 20px;
  margin-bottom: 15px;
}

.readme-section li {
  line-height: 1.6;
  color: #606266;
  margin-bottom: 8px;
}

.api-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.api-table th,
.api-table td {
  border: 1px solid #e4e7ed;
  padding: 10px;
  text-align: left;
}

.api-table th {
  background-color: #f5f7fa;
  font-weight: bold;
  color: #303133;
}

.api-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.api-subsection {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px dashed #e4e7ed;
}

.api-subsection:first-child {
  margin-top: 0;
  padding-top: 0;
  border-top: none;
}
</style>