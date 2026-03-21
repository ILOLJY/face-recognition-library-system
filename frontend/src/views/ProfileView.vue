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
            </div>
          </template>
          <div class="face-info">
            <div class="face-image" v-if="userInfo.faceImage">
              <img :src="userInfo.faceImage" alt="人脸照片">
            </div>
            <div class="face-actions">
              <el-button type="primary" @click="uploadFace">上传人脸照片</el-button>
              <el-button type="success" @click="verifyFace">人脸验证</el-button>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { userApi, authApi } from '../api/index.js'

const router = useRouter()
const userInfo = ref({
  username: 'testuser',
  email: 'test@example.com',
  role: '普通用户',
  createdAt: '2026-03-18',
  faceImage: ''
})

const loading = ref(false)

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
    userInfo.value = {
      ...data,
      role: data.role === 'admin' ? '管理员' : '普通用户',
      createdAt: new Date(data.created_at).toLocaleString()
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    alert('获取用户信息失败：' + (error.response?.data?.detail || '请检查网络连接'))
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
      alert('用户名修改成功')
    }
  } catch (error) {
    console.error('修改用户名失败:', error)
    alert('修改用户名失败：' + (error.response?.data?.detail || '请检查网络连接'))
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
        alert('密码修改成功')
      } catch (error) {
        console.error('修改密码失败:', error)
        alert('修改密码失败：' + (error.response?.data?.detail || '请检查网络连接'))
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

const uploadFace = async () => {
  try {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.onchange = async (e) => {
      const file = e.target.files[0]
      if (file) {
        loading.value = true
        try {
          const data = await userApi.uploadAvatar(file)
          console.log('上传头像成功:', data)
          userInfo.value = {
            ...userInfo.value,
            faceImage: data.avatar
          }
          alert('头像上传成功')
        } catch (error) {
          console.error('上传头像失败:', error)
          alert('上传头像失败：' + (error.response?.data?.detail || '请检查网络连接'))
        } finally {
          loading.value = false
        }
      }
    }
    input.click()
  } catch (error) {
    console.error('上传人脸照片失败:', error)
    alert('上传人脸照片失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

const verifyFace = () => {
  console.log('人脸验证')
  // 这里需要实现人脸验证逻辑
  alert('人脸验证功能开发中')
}

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

.face-actions {
  display: flex;
  gap: 10px;
}
</style>
