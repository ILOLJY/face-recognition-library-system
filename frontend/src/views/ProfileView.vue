<template>
  <div class="profile">
    <el-container>
      <el-main>
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
          <el-button type="default" @click="router.push('/home')">
            <el-icon><ArrowLeft /></el-icon>
            返回主页
          </el-button>
          <h2>个人中心</h2>
        </div>
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <el-form :model="userInfo" label-width="80px">
            <el-form-item label="用户名">
              <el-input v-model="userInfo.username" disabled></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email" disabled></el-input>
            </el-form-item>
            <el-form-item label="角色">
              <el-input v-model="userInfo.role" disabled></el-input>
            </el-form-item>
            <el-form-item label="注册时间">
              <el-input v-model="userInfo.createdAt" disabled></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="editProfile">编辑资料</el-button>
              <el-button type="warning" @click="openPasswordDialog">修改密码</el-button>
              <el-button @click="logout">退出登录</el-button>
            </el-form-item>
          </el-form>
        </el-card>
        <el-card shadow="hover" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>人脸信息</span>
              <el-tag v-if="userInfo.hasFaceData" type="success" size="small">已录入</el-tag>
              <el-tag v-else type="info" size="small">未录入</el-tag>
            </div>
          </template>
          <div class="face-info">
            <div class="face-image" v-if="userInfo.faceImage">
              <img :src="userInfo.faceImage" alt="人脸照片">
            </div>
            <div class="face-placeholder" v-else>
              <el-icon :size="40"><Camera /></el-icon>
              <p>暂无人脸照片</p>
            </div>
            <div class="face-actions">
              <el-button type="primary" @click="openCamera" :loading="loading">
                <el-icon><VideoCamera /></el-icon>
                {{ userInfo.hasFaceData ? '重新录入人脸' : '录入人脸' }}
              </el-button>
              <el-button 
                v-if="userInfo.hasFaceData" 
                type="danger" 
                @click="deleteFaceData" 
                :loading="loading"
              >
                删除人脸
              </el-button>
              <el-button 
                v-if="userInfo.hasFaceData" 
                type="success" 
                @click="verifyFace"
              >
                人脸验证
              </el-button>
            </div>
          </div>
        </el-card>
      </el-main>
    </el-container>
  </div>

  <!-- 密码修改弹窗 -->
  <el-dialog
    v-model="passwordDialogVisible"
    title="修改密码"
    width="400px"
  >
    <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px">
      <el-form-item label="旧密码" prop="oldPassword">
        <el-input v-model="passwordForm.oldPassword" type="password" placeholder="请输入旧密码"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newPassword">
        <el-input v-model="passwordForm.newPassword" type="password" placeholder="请输入新密码"></el-input>
      </el-form-item>
      <el-form-item label="确认新密码" prop="confirmPassword">
        <el-input v-model="passwordForm.confirmPassword" type="password" placeholder="请确认新密码"></el-input>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="updatePassword" :loading="passwordLoading">确定</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 摄像头拍照弹窗 -->
  <el-dialog
    v-model="cameraDialogVisible"
    title="录入人脸"
    width="680px"
    :before-close="closeCamera"
  >
    <div class="camera-container">
      <div class="video-wrapper">
        <video 
          ref="videoElement" 
          autoplay 
          playsinline
          class="video-preview"
        ></video>
        <canvas ref="canvasElement" style="display: none;"></canvas>
        
        <!-- 提示框 -->
        <div class="face-guide" v-if="isCameraOpen">
          <div class="guide-box">
            <p>请将人脸置于框内</p>
          </div>
        </div>
      </div>
      
      <div class="camera-tips">
        <el-alert
          title="提示"
          type="info"
          :closable="false"
        >
          <template #default>
            <ul>
              <li>请确保光线充足</li>
              <li>请正对摄像头</li>
              <li>保持面部完整清晰</li>
            </ul>
          </template>
        </el-alert>
      </div>
    </div>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeCamera">取消</el-button>
        <el-button 
          type="primary" 
          @click="takePhoto" 
          :disabled="!isCameraOpen"
          :loading="loading"
        >
          <el-icon><Camera /></el-icon>
          拍照
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Camera, VideoCamera } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { userApi, authApi, faceApi } from '../api/index.js'

const router = useRouter()
const userInfo = ref({
  username: 'testuser',
  email: 'test@example.com',
  role: '普通用户',
  createdAt: '2026-03-18',
  faceImage: '',
  hasFaceData: false
})

const loading = ref(false)

// 摄像头相关
const cameraDialogVisible = ref(false)
const videoElement = ref(null)
const canvasElement = ref(null)
const stream = ref(null)
const isCameraOpen = ref(false)

// 密码修改相关
const passwordDialogVisible = ref(false)
const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})
const passwordFormRef = ref(null)
const passwordLoading = ref(false)

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' },
    { min: 6, message: '旧密码长度至少 6 个字符', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '新密码长度至少 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const fetchUserInfo = async () => {
  loading.value = true
  try {
    console.log('获取用户信息')
    const data = await userApi.getProfile()
    console.log('获取用户信息成功:', data)
    
    // 尝试获取人脸数据
    let hasFaceData = false
    let faceImage = ''
    try {
      const faceData = await faceApi.getFaceData()
      if (faceData && faceData.face_image_path) {
        hasFaceData = true
        faceImage = 'http://localhost:8000' + faceData.face_image_path
      }
    } catch (error) {
      console.log('未检测到人脸数据')
    }
    
    userInfo.value = {
      ...data,
      role: data.role === 'admin' ? '管理员' : '普通用户',
      createdAt: new Date(data.created_at).toLocaleString(),
      hasFaceData,
      faceImage
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    ElMessage.error('获取用户信息失败：' + (error.response?.data?.detail || '请检查网络连接'))
  } finally {
    loading.value = false
  }
}

const editProfile = async () => {
  try {
    const newUsername = prompt('请输入新用户名:', userInfo.value.username)
    if (newUsername && newUsername.trim()) {
      loading.value = true
      const data = await userApi.updateUsername(newUsername.trim())
      console.log('修改用户名成功:', data)
      userInfo.value = {
        ...userInfo.value,
        username: data.username
      }
      ElMessage.success('用户名修改成功')
    }
  } catch (error) {
    console.error('修改用户名失败:', error)
    ElMessage.error('修改用户名失败：' + (error.response?.data?.detail || '请检查网络连接'))
  } finally {
    loading.value = false
  }
}

const logout = async () => {
  console.log('执行注销登录')
  try {
    await authApi.logout()
    console.log('注销成功')
    router.push('/login')
  } catch (error) {
    console.error('注销失败:', error)
    // 即使失败也跳转到登录页面
    router.push('/login')
  }
}

const openPasswordDialog = () => {
  // 重置表单
  passwordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  if (passwordFormRef.value) {
    passwordFormRef.value.resetFields()
  }
  // 打开弹窗
  passwordDialogVisible.value = true
}

const updatePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      passwordLoading.value = true
      try {
        console.log('修改密码')
        await userApi.updatePassword(
          passwordForm.value.oldPassword,
          passwordForm.value.newPassword
        )
        console.log('修改密码成功')
        passwordDialogVisible.value = false
        ElMessage.success('密码修改成功')
      } catch (error) {
        console.error('修改密码失败:', error)
        ElMessage.error('修改密码失败：' + (error.response?.data?.detail || '请检查网络连接'))
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

// 打开摄像头
const openCamera = async () => {
  cameraDialogVisible.value = true
  
  // 等待 DOM 更新
  setTimeout(async () => {
    try {
      stream.value = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: 'user' // 前置摄像头
        }
      })
      
      if (videoElement.value) {
        videoElement.value.srcObject = stream.value
        await videoElement.value.play()
        isCameraOpen.value = true
      }
    } catch (error) {
      console.error('无法访问摄像头:', error)
      ElMessage.error('无法访问摄像头，请确保已授权摄像头权限')
      cameraDialogVisible.value = false
    }
  }, 100)
}

// 关闭摄像头
const closeCamera = () => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
    stream.value = null
  }
  isCameraOpen.value = false
  cameraDialogVisible.value = false
}

// 拍照
const takePhoto = async () => {
  if (!videoElement.value || !canvasElement.value) {
    ElMessage.error('摄像头未就绪')
    return
  }
  
  const video = videoElement.value
  const canvas = canvasElement.value
  const context = canvas.getContext('2d')
  
  // 设置 canvas 尺寸与视频一致
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  
  // 绘制当前帧到 canvas
  context.drawImage(video, 0, 0, canvas.width, canvas.height)
  
  // 转换为 blob
  canvas.toBlob(async (blob) => {
    if (!blob) {
      ElMessage.error('拍照失败')
      return
    }
    
    // 创建 File 对象
    const file = new File([blob], `face_${Date.now()}.jpg`, { type: 'image/jpeg' })
    
    // 上传到服务器
    await uploadFacePhoto(file)
  }, 'image/jpeg', 0.9)
}

// 上传人脸照片
const uploadFacePhoto = async (file) => {
  loading.value = true
  try {
    console.log('上传人脸照片:', file)
    const data = await faceApi.registerFace(file)
    console.log('上传人脸照片成功:', data)
    
    // 更新人脸信息
    userInfo.value.hasFaceData = true
    if (data.face_image_path) {
      userInfo.value.faceImage = 'http://localhost:8000' + data.face_image_path
    }
    
    ElMessage.success('人脸照片上传成功')
    closeCamera()
  } catch (error) {
    console.error('上传人脸照片失败:', error)
    ElMessage.error('上传人脸照片失败：' + (error.response?.data?.detail || '请检查网络连接'))
  } finally {
    loading.value = false
  }
}

// 删除人脸数据
const deleteFaceData = async () => {
  if (!confirm('确定要删除人脸数据吗？')) {
    return
  }
  
  loading.value = true
  try {
    await faceApi.deleteFaceData()
    userInfo.value.hasFaceData = false
    userInfo.value.faceImage = ''
    ElMessage.success('人脸数据删除成功')
  } catch (error) {
    console.error('删除人脸数据失败:', error)
    ElMessage.error('删除人脸数据失败：' + (error.response?.data?.detail || '请检查网络连接'))
  } finally {
    loading.value = false
  }
}

const verifyFace = () => {
  console.log('人脸验证')
  // 这里需要实现人脸验证逻辑
  ElMessage.info('人脸验证功能开发中')
}

// 组件卸载时清理
onBeforeUnmount(() => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
  }
})

onMounted(() => {
  // 从后端获取用户信息
  fetchUserInfo()
})
</script>

<style scoped>
.profile {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.profile h2 {
  margin-bottom: 30px;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.face-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.face-image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e4e7ed;
}

.face-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.face-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  border: 2px dashed #dcdfe6;
}

.face-placeholder p {
  margin-top: 5px;
  font-size: 12px;
}

.face-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* 摄像头样式 */
.camera-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.video-wrapper {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-preview {
  width: 100%;
  height: 480px;
  object-fit: cover;
  display: block;
}

.face-guide {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.guide-box {
  width: 280px;
  height: 350px;
  border: 3px dashed rgba(255, 255, 255, 0.6);
  border-radius: 50%;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 20px;
}

.guide-box p {
  color: #fff;
  background: rgba(0, 0, 0, 0.6);
  padding: 5px 15px;
  border-radius: 15px;
  font-size: 14px;
}

.camera-tips ul {
  margin: 0;
  padding-left: 20px;
}

.camera-tips li {
  margin: 5px 0;
  color: #606266;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
