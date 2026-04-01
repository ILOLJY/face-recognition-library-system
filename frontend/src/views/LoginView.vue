<template>
  <div class="login">
    <el-container>
      <el-main>
        <div class="login-form">
          <h2>用户登录</h2>
          <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
            <el-form-item label="邮箱" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="login" :loading="loading">登录</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
            <div class="face-login">
              <el-button type="success" @click="openFaceLogin" style="width: 100%">
                <el-icon><Camera /></el-icon>
                人脸登录
              </el-button>
            </div>
            <div class="register-link">
              还没有账号？<router-link to="/register">立即注册</router-link>
            </div>
            <div class="admin-login">
              <el-button type="info" @click="goToAdminLogin" style="width: 100%">
                管理员登录
              </el-button>
            </div>
            <div class="readme-link">
              <el-button link @click="goToReadme">查看系统文档</el-button>
            </div>
          </el-form>
        </div>
      </el-main>
    </el-container>

    <!-- 人脸登录弹窗 -->
    <el-dialog
      v-model="faceLoginDialogVisible"
      title="人脸登录"
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
            @click="takePhotoAndLogin" 
            :disabled="!isCameraOpen"
            :loading="loading"
          >
            <el-icon><Camera /></el-icon>
            拍照登录
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onBeforeUnmount, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Camera } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { authApi, faceApi } from '../api/index.js'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

// 摄像头相关
const faceLoginDialogVisible = ref(false)
const videoElement = ref(null)
const canvasElement = ref(null)
const stream = ref(null)
const isCameraOpen = ref(false)

// 快速登录相关
const quickLoginEmail = ref('')
const quickLoginNickname = ref('')

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ]
}

const login = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      console.log('开始登录，邮箱:', loginForm.username)
      try {
        // 调用后端登录接口
        console.log('调用 /api/auth/login 接口')
        const data = await authApi.login({
          email: loginForm.username, // 前端用户名输入框实际输入的是邮箱
          password: loginForm.password
        })
        
        console.log('登录成功，返回数据:', data)
        console.log('当前cookie:', document.cookie)
        
        // 保存邮箱和昵称到 localStorage
        localStorage.setItem('lastLoginEmail', loginForm.username)
        localStorage.setItem('lastLoginNickname', data.user.username)
        
        loading.value = false
        
        // 后端已经设置了 HttpOnly cookie，直接跳转
        console.log('登录成功，跳转到首页')
        router.push('/home')
      } catch (error) {
        loading.value = false
        console.error('登录失败:', error.response?.data || error.message)
        ElMessage.error('登录失败：' + (error.response?.data?.detail || '请检查邮箱和密码'))
      }
    }
  })
}

const resetForm = () => {
  if (loginFormRef.value) {
    loginFormRef.value.resetFields()
  }
}

const goToAdminLogin = () => {
  console.log('跳转到管理员登录页面')
  router.push('/admin/login')
}

const goToReadme = () => {
  console.log('跳转到系统文档')
  router.push('/readme')
}

// 打开摄像头（人脸登录）
const openFaceLogin = async () => {
  // 验证邮箱是否已填写
  if (!loginForm.username) {
    ElMessage.warning('请先输入邮箱')
    return
  }
  
  faceLoginDialogVisible.value = true
  
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
      faceLoginDialogVisible.value = false
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
  faceLoginDialogVisible.value = false
}

// 拍照并登录
const takePhotoAndLogin = async () => {
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
    const file = new File([blob], `face_login_${Date.now()}.jpg`, { type: 'image/jpeg' })
    
    // 调用人脸登录接口
    await performFaceLogin(file)
  }, 'image/jpeg', 0.9)
}

// 执行人脸登录
const performFaceLogin = async (file) => {
  loading.value = true
  try {
    console.log('人脸登录，邮箱:', loginForm.username)
    const data = await faceApi.login(loginForm.username, file)
    console.log('人脸登录成功:', data)
    
    // 保存邮箱和昵称到 localStorage
    localStorage.setItem('lastLoginEmail', loginForm.username)
    localStorage.setItem('lastLoginNickname', data.user.username)
    
    ElMessage.success('人脸登录成功')
    closeCamera()
    
    // 登录成功，跳转到首页
    router.push('/home')
  } catch (error) {
    console.error('人脸登录失败:', error)
    ElMessage.error('人脸登录失败：' + (error.response?.data?.detail || '请重试'))
  } finally {
    loading.value = false
  }
}

// 组件卸载时清理
onBeforeUnmount(() => {
  if (stream.value) {
    stream.value.getTracks().forEach(track => track.stop())
  }
})

// 组件挂载时检查快速登录
onMounted(async () => {
  const savedEmail = localStorage.getItem('lastLoginEmail')
  const savedNickname = localStorage.getItem('lastLoginNickname')
  
  if (savedEmail && savedNickname) {
    quickLoginEmail.value = savedEmail
    quickLoginNickname.value = savedNickname
    
    // 自动填充邮箱
    loginForm.username = savedEmail
    
    // 显示快速登录提示
    ElMessageBox.confirm(
      `检测到您上次登录的账号：${savedNickname}，是否使用人脸快速登录？`,
      '快速登录',
      {
        confirmButtonText: '人脸登录',
        cancelButtonText: '密码登录',
        type: 'info'
      }
    ).then(() => {
      // 用户选择人脸登录
      openFaceLogin()
    }).catch(() => {
      // 用户选择密码登录，不做任何操作
    })
  }
})
</script>

<style scoped>
.login {
  min-height: 100vh;
  background: #f5f7fa;
}

.login-form {
  max-width: 400px;
  margin: 100px auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.login-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #409EFF;
}

.face-login {
  margin-top: 15px;
  text-align: center;
}

.register-link {
  text-align: center;
  margin-top: 20px;
}

.register-link a {
  color: #409EFF;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.admin-login {
  margin-top: 20px;
}

.readme-link {
  margin-top: 20px;
  text-align: center;
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
