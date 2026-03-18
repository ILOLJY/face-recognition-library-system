<template>
  <div class="borrow">
    <el-container>
      <el-main>
        <h2>借阅记录</h2>
        <el-table :data="borrowRecords" style="width: 100%">
          <el-table-column prop="id" label="记录ID" width="80"></el-table-column>
          <el-table-column prop="bookTitle" label="图书名称" width="200"></el-table-column>
          <el-table-column prop="borrowDate" label="借阅日期"></el-table-column>
          <el-table-column prop="dueDate" label="应还日期"></el-table-column>
          <el-table-column prop="returnDate" label="实际归还日期"></el-table-column>
          <el-table-column prop="status" label="状态">
            <template #default="scope">
              <el-tag :type="getStatusType(scope.row.status)">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="primary" size="small" @click="returnBook(scope.row)" v-if="scope.row.status === 'BORROWED'">
                归还
              </el-button>
              <el-button type="warning" size="small" @click="renewBook(scope.row)" v-if="scope.row.status === 'BORROWED'">
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
import axios from 'axios'

const borrowRecords = ref([
  {
    id: 1,
    bookTitle: 'Python 编程从入门到实践',
    borrowDate: '2026-03-01',
    dueDate: '2026-03-15',
    returnDate: null,
    status: 'BORROWED'
  },
  {
    id: 2,
    bookTitle: '深入理解计算机系统',
    borrowDate: '2026-02-15',
    dueDate: '2026-03-01',
    returnDate: '2026-02-28',
    status: 'RETURNED'
  }
])

const getStatusType = (status) => {
  switch (status) {
    case 'BORROWED': return 'primary'
    case 'RETURNED': return 'success'
    case 'OVERDUE': return 'danger'
    case 'RENEWED': return 'warning'
    default: return 'info'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'BORROWED': return '借阅中'
    case 'RETURNED': return '已归还'
    case 'OVERDUE': return '逾期'
    case 'RENEWED': return '已续借'
    default: return status
  }
}

const returnBook = (record) => {
  console.log('归还图书:', record)
  // 这里需要实现归还逻辑
}

const renewBook = (record) => {
  console.log('续借图书:', record)
  // 这里需要实现续借逻辑
}

onMounted(() => {
  // 这里需要从后端获取借阅记录
  // fetchBorrowRecords()
})

const fetchBorrowRecords = async () => {
  try {
    // const response = await axios.get('/api/borrow/records')
    // borrowRecords.value = response.data
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
