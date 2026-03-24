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
          
          <el-table :data="books" style="width: 100%" :loading="loading">
            <el-table-column prop="id" label="图书ID" width="80"></el-table-column>
            <el-table-column prop="title" label="图书名称" width="200"></el-table-column>
            <el-table-column prop="author" label="作者"></el-table-column>
            <el-table-column prop="category" label="分类"></el-table-column>
            <el-table-column prop="total_copies" label="总册数" width="100"></el-table-column>
            <el-table-column prop="available_copies" label="可借册数" width="100"></el-table-column>
            <el-table-column prop="location" label="位置" width="120"></el-table-column>
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'available' ? 'success' : 'danger'">
                  {{ scope.row.status === 'available' ? '可借阅' : '已借出' }}
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
        <el-form-item label="ISBN">
          <el-input v-model="bookForm.isbn" placeholder="请输入ISBN"></el-input>
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="bookForm.publisher" placeholder="请输入出版社"></el-input>
        </el-form-item>
        <el-form-item label="出版日期">
          <el-date-picker
            v-model="bookForm.publish_date"
            type="date"
            placeholder="选择出版日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="分类">
          <el-input v-model="bookForm.category" placeholder="请输入分类"></el-input>
        </el-form-item>
        <el-form-item label="简介">
          <el-input
            v-model="bookForm.description"
            type="textarea"
            placeholder="请输入图书简介"
            :rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="总册数" prop="total_copies">
          <el-input-number v-model="bookForm.total_copies" :min="1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="可借阅册数" prop="available_copies">
          <el-input-number v-model="bookForm.available_copies" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="存放位置">
          <el-input v-model="bookForm.location" placeholder="请输入存放位置"></el-input>
        </el-form-item>
        <el-form-item label="封面">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :http-request="handleCoverUpload"
          >
            <img v-if="bookForm.cover_image" :src="bookForm.cover_image" class="avatar" />
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
import { ElMessage } from 'element-plus'
import { bookApi } from '../api/index.js'

const router = useRouter()

// 图书列表
const books = ref([])
const loading = ref(false)

// 弹窗相关
const bookDialogVisible = ref(false)
const isEdit = ref(false)
const bookForm = ref({
  id: '',
  title: '',
  author: '',
  isbn: '',
  publisher: '',
  publish_date: '',
  category: '',
  description: '',
  total_copies: 1,
  available_copies: 1,
  location: ''
})
const bookFormRef = ref(null)
const bookLoading = ref(false)

// 表单验证规则
const bookRules = {
  title: [
    { required: true, message: '请输入图书名称', trigger: 'blur' },
    { min: 1, max: 200, message: '图书名称长度在 1 到 200 个字符', trigger: 'blur' }
  ],
  author: [
    { required: true, message: '请输入作者', trigger: 'blur' },
    { min: 1, max: 100, message: '作者长度在 1 到 100 个字符', trigger: 'blur' }
  ],
  total_copies: [
    { required: true, message: '请输入总册数', trigger: 'blur' },
    { type: 'number', min: 1, message: '总册数必须大于等于1', trigger: 'blur' }
  ],
  available_copies: [
    { required: true, message: '请输入可借阅册数', trigger: 'blur' },
    { type: 'number', min: 0, message: '可借阅册数必须大于等于0', trigger: 'blur' }
  ]
}

// 打开添加图书弹窗
const openAddBookDialog = () => {
  isEdit.value = false
  bookForm.value = {
    id: '',
    title: '',
    author: '',
    isbn: '',
    publisher: '',
    publish_date: '',
    category: '',
    description: '',
    total_copies: 1,
    available_copies: 1,
    location: ''
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
          await bookApi.updateBook(bookForm.value.id, bookForm.value)
          ElMessage.success('图书编辑成功')
        } else {
          // 添加图书
          await bookApi.addBook(bookForm.value)
          ElMessage.success('图书添加成功')
        }
        bookDialogVisible.value = false
        // 重新获取图书列表
        fetchBooks()
      } catch (error) {
        console.error('操作失败:', error)
        let errorMessage = '请检查网络连接'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
          // 处理ISBN重复的情况
          if (errorMessage.includes('重复键违反唯一约束') && errorMessage.includes('isbn')) {
            errorMessage = '该ISBN编号已存在，请使用不同的ISBN'
          }
        }
        ElMessage.error('操作失败：' + errorMessage)
      } finally {
        bookLoading.value = false
      }
    }
  })
}

// 删除图书
const deleteBook = async (bookId) => {
  try {
    await bookApi.deleteBook(bookId)
    ElMessage.success('图书删除成功')
    // 重新获取图书列表
    fetchBooks()
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

// 处理封面上传
const handleCoverUpload = async (file) => {
  if (!bookForm.value.id) {
    ElMessage.error('请先保存图书信息，再上传封面')
    return
  }
  
  try {
    await bookApi.uploadCover(bookForm.value.id, file.file)
    ElMessage.success('封面上传成功')
    // 重新获取图书列表
    fetchBooks()
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败：' + (error.response?.data?.detail || '请检查网络连接'))
  }
}

// 获取图书列表
const fetchBooks = async () => {
  loading.value = true
  try {
    const data = await bookApi.getAllBooks()
    books.value = data
  } catch (error) {
    console.error('获取图书列表失败:', error)
    ElMessage.error('获取图书列表失败：' + (error.response?.data?.detail || '请检查网络连接'))
  } finally {
    loading.value = false
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