<template>
  <div class="login">
    <el-container>
      <el-main>
        <div class="login-form">
          <h2>管理员登录</h2>
          <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
            <el-form-item label="邮箱" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入管理员邮箱"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入管理员密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="login" :loading="loading">登录</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
            <div class="user-login">
              <el-button type="default" @click="goToUserLogin" style="width: 100%">
                用户登录
              </el-button>
            </div>
          </el-form>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/index.js'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { min: 3, max: 50, message: '邮箱长度在 3 到 50 个字符', trigger: 'blur' }
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
      console.log('开始管理员登录，邮箱:', loginForm.username)
      try {
        // 调用后端管理员登录接口
        console.log('调用 /api/auth/admin/login 接口')
        const data = await authApi.adminLogin({
          email: loginForm.username,
          password: loginForm.password
        })
        
        console.log('管理员登录成功，返回数据:', data)
        console.log('当前cookie:', document.cookie)
        loading.value = false
        
        // 后端已经设置了 HttpOnly cookie，直接跳转到管理员页面
        console.log('管理员登录成功，跳转到管理员页面')
        router.push('/admin')
      } catch (error) {
        loading.value = false
        console.error('管理员登录失败:', error.response?.data || error.message)
        alert('管理员登录失败：' + (error.response?.data?.detail || '请检查邮箱和密码'))
      }
    }
  })
}

const resetForm = () => {
  if (loginFormRef.value) {
    loginFormRef.value.resetFields()
  }
}

const goToUserLogin = () => {
  console.log('跳转到用户登录页面')
  router.push('/login')
}
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

.user-login {
  margin-top: 20px;
}
</style>