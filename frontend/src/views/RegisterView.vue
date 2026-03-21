<template>
  <div class="register">
    <el-container>
      <el-main>
        <div class="register-form">
          <h2>用户注册</h2>
          <el-form :model="registerForm" :rules="rules" ref="registerFormRef" label-width="80px">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input v-model="registerForm.password" type="password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="验证码" prop="code">
              <el-row :gutter="10">
                <el-col :span="16">
                  <el-input v-model="registerForm.code" placeholder="请输入验证码"></el-input>
                </el-col>
                <el-col :span="8">
                  <el-button 
                    :disabled="countdown > 0" 
                    @click="sendCode"
                    type="primary"
                  >
                    {{ countdown > 0 ? `${countdown}秒后重发` : '发送验证码' }}
                  </el-button>
                </el-col>
              </el-row>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="register" :loading="loading">注册</el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
            <div class="login-link">
              已有账号？<router-link to="/login">立即登录</router-link>
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
const registerFormRef = ref(null)
const loading = ref(false)
const countdown = ref(0)

const registerForm = reactive({
  username: '',
  password: '',
  email: '',
  code: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3 到 50 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { length: 6, message: '验证码长度为 6 位', trigger: 'blur' }
  ]
}

const sendCode = async () => {
  if (!registerForm.email) {
    return
  }
  
  try {
    // 发送验证码
    await authApi.sendVerificationCode(registerForm.email)
    
    // 倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
    
    alert('验证码已发送到您的邮箱')
  } catch (error) {
    console.error('发送验证码失败:', error)
    alert('发送验证码失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

const register = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // 调用后端注册接口
        const data = await authApi.register({
          username: registerForm.username,
          password: registerForm.password,
          email: registerForm.email,
          code: registerForm.code,
          avatar: '',
          role: 'user'
        })
        
        loading.value = false
        alert('注册成功！请登录')
        router.push('/login')
      } catch (error) {
        loading.value = false
        console.error('注册失败:', error)
        alert('注册失败：' + (error.response?.data?.detail || '请检查注册信息'))
      }
    }
  })
}

const resetForm = () => {
  if (registerFormRef.value) {
    registerFormRef.value.resetFields()
  }
}
</script>

<style scoped>
.register {
  min-height: 100vh;
  background: #f5f7fa;
}

.register-form {
  max-width: 400px;
  margin: 60px auto;
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.register-form h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #409EFF;
}

.login-link {
  text-align: center;
  margin-top: 20px;
}

.login-link a {
  color: #409EFF;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
