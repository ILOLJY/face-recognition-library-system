<template>
  <div class="borrow">
    <el-container>
      <el-main>
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
          <el-button type="default" @click="router.push('/home')">
            <el-icon><ArrowLeft /></el-icon>
            返回主页
          </el-button>
          <h2>借阅记录</h2>
        </div>
        <el-table :data="borrowRecords" style="width: 100%">
          <el-table-column prop="id" label="记录ID" width="80"></el-table-column>
          <el-table-column label="图书名称" width="200">
            <template #default="scope">
              {{ scope.row.book_title || '未知' }}
            </template>
          </el-table-column>
          <el-table-column label="借阅日期">
            <template #default="scope">
              {{ formatDate(scope.row.borrow_date) }}
            </template>
          </el-table-column>
          <el-table-column label="应还日期">
            <template #default="scope">
              {{ formatDate(scope.row.due_date) }}
            </template>
          </el-table-column>
          <el-table-column label="实际归还日期">
            <template #default="scope">
              {{ formatDate(scope.row.return_date) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="primary" size="small" @click="returnBook(scope.row)" v-if="['borrowed', 'renewed', 'overdue'].includes(scope.row.status)">
                归还
              </el-button>
              <el-button type="warning" size="small" @click="renewBook(scope.row)" v-if="['borrowed', 'overdue'].includes(scope.row.status)">
                续借
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()

const borrowRecords = ref([])

// 日期格式化函数
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusType = (status) => {
  const statusLower = status.toLowerCase()
  switch (statusLower) {
    case 'borrowed': return 'primary'
    case 'returned': return 'success'
    case 'overdue': return 'danger'
    case 'renewed': return 'warning'
    default: return 'info'
  }
}

const getStatusText = (status) => {
  const statusLower = status.toLowerCase()
  switch (statusLower) {
    case 'borrowed': return '借阅中'
    case 'returned': return '已归还'
    case 'overdue': return '逾期'
    case 'renewed': return '已续借'
    default: return status
  }
}

const returnBook = async (record) => {
  try {
    await axios.post(`/api/borrow/return/${record.id}`)
    ElMessage.success('归还成功')
    // 重新获取借阅记录
    fetchBorrowRecords()
  } catch (error) {
    console.error('归还失败:', error)
    ElMessage.error('归还失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

const renewBook = async (record) => {
  try {
    await axios.post(`/api/borrow/renew/${record.id}`)
    ElMessage.success('续借成功')
    // 重新获取借阅记录
    fetchBorrowRecords()
  } catch (error) {
    console.error('续借失败:', error)
    ElMessage.error('续借失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

onMounted(() => {
  // 从后端获取借阅记录
  fetchBorrowRecords()
})

const fetchBorrowRecords = async () => {
  try {
    const response = await axios.get('/api/borrow/records')
    borrowRecords.value = response.data
  } catch (error) {
    console.error('获取借阅记录失败:', error)
  }
}
</script>

<style scoped>
.borrow {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.borrow h2 {
  margin-bottom: 30px;
  color: #303133;
}
</style>
