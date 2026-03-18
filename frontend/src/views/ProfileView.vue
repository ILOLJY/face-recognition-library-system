<template>
  <div class="profile">
    <el-container>
      <el-main>
        <h2>个人中心</h2>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const userInfo = ref({
  username: 'testuser',
  email: 'test@example.com',
  role: '普通用户',
  createdAt: '2026-03-18',
  faceImage: ''
})

const editProfile = () => {
  console.log('编辑资料')
  // 这里需要实现编辑资料逻辑
}

const logout = () => {
  console.log('退出登录')
  // 这里需要实现退出登录逻辑
  router.push('/login')
}

const uploadFace = () => {
  console.log('上传人脸照片')
  // 这里需要实现上传人脸照片逻辑
}

const verifyFace = () => {
  console.log('人脸验证')
  // 这里需要实现人脸验证逻辑
}

onMounted(() => {
  // 这里需要从后端获取用户信息
  // fetchUserInfo()
})

const fetchUserInfo = async () => {
  try {
    // const response = await axios.get('/api/users/profile')
    // userInfo.value = response.data
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}
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
