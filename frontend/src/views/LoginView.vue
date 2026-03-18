<template>
  <div class="login">
    <el-container>
      <el-main>
        <div class="login-form">
          <h2>用户登录</h2>
          <el-form :model="loginForm" :rules="rules" ref="loginFormRef" label-width="80px">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="login" :loading="loading">登录</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
            <div class="register-link">
              还没有账号？<router-link to="/register">立即注册</router-link>
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
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

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
      try {
        // 这里需要实现登录逻辑
        // const response = await axios.post('/api/auth/login', loginForm)
        // 模拟登录成功
        setTimeout(() => {
          loading.value = false
          router.push('/')
        }, 1000)
      } catch (error) {
        loading.value = false
        console.error('登录失败:', error)
      }
    }
  })
}

const resetForm = () => {
  if (loginFormRef.value) {
    loginFormRef.value.resetFields()
  }
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
</style>
