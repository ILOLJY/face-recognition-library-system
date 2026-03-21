<template>
  <div class="admin">
    <el-container>
      <el-main>
        <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 30px;">
          <el-button type="default" @click="router.push('/home')">
            <el-icon><ArrowLeft /></el-icon>
            返回主页
          </el-button>
          <h2>管理员中心</h2>
        </div>
        
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>图书管理</span>
              <el-button type="primary" @click="openAddBookDialog">添加图书</el-button>
            </div>
          </template>
          
          <el-table :data="books" style="width: 100%">
            <el-table-column prop="id" label="图书ID" width="80"></el-table-column>
            <el-table-column prop="title" label="图书名称" width="200"></el-table-column>
            <el-table-column prop="author" label="作者"></el-table-column>
            <el-table-column prop="category" label="分类"></el-table-column>
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'AVAILABLE' ? 'success' : 'danger'">
                  {{ scope.row.status === 'AVAILABLE' ? '可借阅' : '已借出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editBook(scope.row)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="deleteBook(scope.row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
    </el-container>

    <!-- 添加/编辑图书弹窗 -->
    <el-dialog
      v-model="bookDialogVisible"
      :title="isEdit ? '编辑图书' : '添加图书'"
      width="500px"
    >
      <el-form :model="bookForm" :rules="bookRules" ref="bookFormRef" label-width="100px">
        <el-form-item label="图书名称" prop="title">
          <el-input v-model="bookForm.title" placeholder="请输入图书名称"></el-input>
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="bookForm.author" placeholder="请输入作者"></el-input>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input v-model="bookForm.category" placeholder="请输入分类"></el-input>
        </el-form-item>
        <el-form-item label="封面">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :http-request="handleCoverUpload"
          >
            <img v-if="bookForm.cover" :src="bookForm.cover" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="bookDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveBook" :loading="bookLoading">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

// 图书列表
const books = ref([
  {
    id: 1,
    title: 'Python 编程从入门到实践',
    author: 'Eric Matthes',
    category: '计算机',
    status: 'AVAILABLE',
    cover: ''
  },
  {
    id: 2,
    title: '深入理解计算机系统',
    author: 'Randal E. Bryant',
    category: '计算机',
    status: 'BORROWED',
    cover: ''
  }
])

// 弹窗相关
const bookDialogVisible = ref(false)
const isEdit = ref(false)
const bookForm = ref({
  id: '',
  title: '',
  author: '',
  category: '',
  cover: ''
})
const bookFormRef = ref(null)
const bookLoading = ref(false)

// 表单验证规则
const bookRules = {
  title: [
    { required: true, message: '请输入图书名称', trigger: 'blur' },
    { min: 1, max: 100, message: '图书名称长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  author: [
    { required: true, message: '请输入作者', trigger: 'blur' },
    { min: 1, max: 50, message: '作者长度在 1 到 50 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请输入分类', trigger: 'blur' },
    { min: 1, max: 30, message: '分类长度在 1 到 30 个字符', trigger: 'blur' }
  ]
}

// 打开添加图书弹窗
const openAddBookDialog = () => {
  isEdit.value = false
  bookForm.value = {
    id: '',
    title: '',
    author: '',
    category: '',
    cover: ''
  }
  if (bookFormRef.value) {
    bookFormRef.value.resetFields()
  }
  bookDialogVisible.value = true
}

// 编辑图书
const editBook = (book) => {
  isEdit.value = true
  bookForm.value = { ...book }
  bookDialogVisible.value = true
}

// 保存图书
const saveBook = async () => {
  if (!bookFormRef.value) return
  
  await bookFormRef.value.validate(async (valid) => {
    if (valid) {
      bookLoading.value = true
      try {
        if (isEdit.value) {
          // 编辑图书
          console.log('编辑图书:', bookForm.value)
          // 调用后端编辑接口
        } else {
          // 添加图书
          console.log('添加图书:', bookForm.value)
          // 调用后端添加接口
        }
        bookDialogVisible.value = false
        alert('操作成功')
        // 重新获取图书列表
        fetchBooks()
      } catch (error) {
        console.error('操作失败:', error)
        alert('操作失败：' + (error.response?.data?.detail || '请检查网络连接'))
      } finally {
        bookLoading.value = false
      }
    }
  })
}

// 删除图书
const deleteBook = (bookId) => {
  console.log('删除图书:', bookId)
  // 调用后端删除接口
}

// 处理封面上传
const handleCoverUpload = (file) => {
  console.log('上传封面:', file)
  // 调用后端上传接口
}

// 获取图书列表
const fetchBooks = async () => {
  try {
    // const response = await axios.get('/api/admin/books')
    // books.value = response.data
  } catch (error) {
    console.error('获取图书列表失败:', error)
  }
}

onMounted(() => {
  // 获取图书列表
  fetchBooks()
})
</script>

<style scoped>
.admin {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px 0;
}

.admin h2 {
  margin: 0;
  color: #303133;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.avatar-uploader:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>