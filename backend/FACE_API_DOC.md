# 人脸识别 API 文档

基于 InsightFace 的人脸识别和注册系统。

## API 接口

### 1. 人脸注册
- **接口**: `POST /api/face/register`
- **描述**: 用户上传人脸图片，系统提取人脸特征并保存到数据库
- **认证**: 需要 JWT 认证（HttpOnly Cookie）
- **请求参数**:
  - `file`: 人脸图片文件（支持 JPG、PNG 格式，最大 5MB）
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "message": "人脸注册成功",
    "face_image_path": "/static/faces/face_1_1711800000.jpg",
    "face_encoding_length": 512
  }
  ```

**使用流程**:
1. 用户登录获取 JWT token
2. 上传人脸图片
3. 系统自动检测人脸、提取特征向量  
4. 保存人脸图片和特征向量到数据库

### 2. 获取人脸数据
- **接口**: `GET /api/face/data`
- **描述**: 获取当前用户的人脸数据
- **认证**: 需要 JWT 认证
- **响应**:
  ```json
  {
    "id": 1,
    "user_id": 1,
    "face_encoding": [0.123, -0.456, 0.789, ...], // 512维特征向量
    "face_image_path": "/static/faces/face_1_1711800000.jpg",
    "created_at": "2026-03-30T10:00:00",
    "updated_at": "2026-03-30T10:00:00"
  }
  ```

### 3. 删除人脸数据
- **接口**: `DELETE /api/face/data`
- **描述**: 删除当前用户的人脸数据（包括图片文件）
- **认证**: 需要 JWT 认证
- **响应**:
  ```json
  {
    "message": "人脸数据删除成功"
  }
  ```

### 4. 验证服务可用性
- **接口**: `GET /api/face/verify`
- **描述**: 验证人脸识别服务是否可用
- **响应**:
  ```json
  {
    "status": "available",
    "message": "人脸识别服务正常运行"
  }
  ```
  或
  ```json
  {
    "status": "unavailable",
    "message": "人脸识别服务不可用: [具体错误信息]"
  }
  ```

## 技术实现

### 人脸注册流程
```
1. 用户上传图片
2. 验证图片类型和大小
3. 使用 InsightFace 检测人脸
4. 提取 512 维人脸特征向量
5. 裁剪并保存人脸图片
6. 将特征向量（JSON格式）和人脸图片路径存入数据库
```

### 数据库模型
```python
class FaceData(Base):
    __tablename__ = "face_data"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True)
    face_encoding: Mapped[List[float]] = mapped_column(JSON, nullable=False)  # JSON 存储
    face_image_path: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
```

### 文件存储结构
```
backend/
├── app/
│   ├── static/
│   │   ├── faces/          # 人脸图片存储目录
│   │   │   ├── face_1_1711800000.jpg
│   │   │   └── face_2_1711800100.jpg
│   │   └── avatars/        # 用户头像
```

## 错误处理

### HTTP 状态码
- `400 Bad Request`: 文件无效、未检测到人脸、文件过大
- `401 Unauthorized`: 未提供有效 JWT token
- `404 Not Found`: 未找到人脸数据
- `503 Service Unavailable`: InsightFace 库不可用

### 常见错误信息
1. **文件相关错误**:
   - "请上传图片文件（支持 JPG、PNG 格式）"
   - "图片文件大小不能超过 5MB"
   - "无法读取图片文件，请检查文件格式"

2. **人脸检测错误**:
   - "未检测到人脸，请确保图片中包含清晰的人脸"
   - "人脸特征提取失败"

3. **服务错误**:
   - "人脸识别服务不可用，请检查 InsightFace 库安装"
   - "保存人脸数据失败"

## 使用示例

### cURL 示例
```bash
# 人脸注册
curl -X POST "http://localhost:8000/api/face/register" \
  -H "Cookie: access_token=<your_jwt_token>" \
  -F "file=@face.jpg"

# 获取人脸数据
curl -X GET "http://localhost:8000/api/face/data" \
  -H "Cookie: access_token=<your_jwt_token>"

# 删除人脸数据
curl -X DELETE "http://localhost:8000/api/face/data" \
  -H "Cookie: access_token=<your_jwt_token>"
```

### Python 示例
```python
import requests

# 设置基础 URL 和认证
BASE_URL = "http://localhost:8000/api/face"
ACCESS_TOKEN = "your_jwt_token_here"
cookies = {"access_token": ACCESS_TOKEN}

# 人脸注册
with open("face.jpg", "rb") as f:
    files = {"file": ("face.jpg", f, "image/jpeg")}
    response = requests.post(f"{BASE_URL}/register", files=files, cookies=cookies)
    print(response.json())

# 获取人脸数据
response = requests.get(f"{BASE_URL}/data", cookies=cookies)
print(response.json())
```

## 依赖库
- `insightface==0.7.3`: 人脸识别核心库
- `opencv-python==4.13.0.92`: 图片处理
- `numpy==2.4.3`: 数值计算
- FastAPI: Web 框架
- SQLAlchemy: 数据库 ORM

## 调试提示

1. **查看人脸特征向量**:
   ```python
   # 在数据库中查看存储的 JSON 格式
   SELECT id, user_id, json_array_length(face_encoding) as dims 
   FROM face_data;
   ```

2. **验证服务**:
   ```bash
   curl "http://localhost:8000/api/face/verify"
   ```

3. **常见问题**:
   - 确保 InsightFace 模型文件已下载
   - 检查上传目录权限 (`app/static/faces/`)
   - 验证数据库 JSON 字段支持

## 安全性考虑

1. **认证**: 使用 JWT token (HttpOnly Cookie)
2. **文件限制**: 限制文件类型和大小
3. **数据隐私**: 人脸数据存储在数据库中，不持久化在磁盘
4. **权限控制**: 用户只能操作自己的人脸数据

## 时区处理决策

### **为什么使用 `datetime.utcnow()` 而不是 `datetime.now(timezone.utc)`**

**问题**: 项目中出现 PostgresQL 错误：`can't subtract offset-naive and offset-aware datetimes`

**原因**: 
1. PostgreSQL 默认使用 **无时区时间戳** (`TIMESTAMP WITHOUT TIME ZONE`)
2. `datetime.now(timezone.utc)` 产生 **有时区的时间**，与数据库不兼容
3. 项目中原有的所有模型都使用 `datetime.utcnow()` 作为默认值

**决策**: 统一使用 `datetime.utcnow()` 无时区时间

**修复位置**:
1. **人脸注册接口**: `created_at=datetime.utcnow()`, `updated_at=datetime.utcnow()`
2. **更新逻辑**: `face_data.updated_at = datetime.utcnow()`
3. **时间戳生成**: `int(datetime.utcnow().timestamp())`

**注意**: 虽然 `datetime.utcnow()` 在 Python 3.12+ 中被弃用，但为了：
- 与原项目保持一致
- 避免 PostgreSQL 时区兼容问题
- 简化开发逻辑

**保持此用法直到数据库迁移到时区感知时间戳**

## 算法优化和关键修复

### 1. **人脸边界框面积计算优化**
**问题**: 原来使用 `bbox[2] * bbox[3]` 计算面积是错误的
**修复**: 正确计算面积为 `(x2 - x1) * (y2 - y1)`
```python
# 修复前（错误）:
faces.sort(key=lambda x: x.bbox[2] * x.bbox[3], reverse=True)

# 修复后（正确）:
faces.sort(
    key=lambda x: (x.bbox[2] - x.bbox[0]) * (x.bbox[3] - x.bbox[1]),
    reverse=True
)
```

### 2. **余弦相似度计算优化**
**问题**: 错误地将相似度裁剪到 [0, 1] 范围
**修复**: 保留余弦相似度的原始范围 [-1, 1]
```python
# 修复前（错误）:
similarity = np.dot(vec1_norm, vec2_norm)
similarity = max(0.0, min(1.0, similarity))  # 错误裁剪

# 修复后（正确）:
similarity = np.dot(vec1_norm, vec2_norm)  # 范围 [-1, 1]

# 使用时可以设置阈值判断:
if similarity > 0.5:  # 建议阈值
    # 认为是同一个人
```

### 3. **特征向量归一化存储**
**优化**: 存储归一化后的特征向量，提高相似度计算稳定性
```python
# 优化前:
embedding = main_face.embedding
embedding_list = embedding.tolist()

# 优化后:
embedding = main_face.embedding
embedding_norm = np.linalg.norm(embedding)
if embedding_norm > 0:
    embedding = embedding / embedding_norm  # 单位化
embedding_list = embedding.tolist()
```

**归一化好处**:
- 相似度计算更稳定
- 数据格式统一
- 减少余弦相似度计算时的归一化步骤

## 性能优化

1. **缓存**: InsightFace 模型单例模式
2. **异步**: 使用 async/await 处理 I/O
3. **批处理**: 支持批量人脸识别（未来扩展）
4. **压缩**: 人脸特征向量存储为 JSON 格式
5. **算法**: 关键算法修复提升准确性和稳定性