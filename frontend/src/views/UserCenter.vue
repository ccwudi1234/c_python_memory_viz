<template>
  <div class="user-center">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="profile-card">
          <template #header>
            <div class="card-header">
              <span>用户信息</span>
            </div>
          </template>
          <div class="profile-info">
            <el-avatar :size="80" :icon="UserFilled" />
            <div class="user-name">{{ userStore.user?.username || '访客' }}</div>
          </div>
          <el-divider />
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-label">分析记录</span>
              <span class="stat-value">{{ userRecords.length }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">上传文件</span>
              <span class="stat-value">{{ userFiles.length }}</span>
            </div>
          </div>
          <el-divider />
          <div class="auth-actions">
            <el-button v-if="!userStore.isLoggedIn" type="primary" @click="showLoginModal = true" style="width: 100%">
              <el-icon><Login /></el-icon> 登录
            </el-button>
            <el-button v-if="!userStore.isLoggedIn" @click="showRegisterModal = true" style="width: 100%; margin-top: 10px">
              <el-icon><UserPlus /></el-icon> 注册
            </el-button>
            <el-button v-if="userStore.isLoggedIn" type="danger" @click="handleLogout" style="width: 100%">
              <el-icon><Logout /></el-icon> 退出登录
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="18">
        <el-card class="records-card">
          <template #header>
            <div class="card-header">
              <span>历史分析记录</span>
            </div>
          </template>
          <el-table :data="userRecords" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="language" label="语言" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.language === 'python' ? 'primary' : 'success'">
                  {{ scope.row.language }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="code_content" label="代码片段" show-overflow-tooltip />
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click="viewRecord(scope.row)">查看</el-button>
                <el-button size="small" type="danger" @click="deleteRecord(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="files-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>我的文件</span>
        </div>
      </template>
      <el-table :data="userFiles" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="file_name" label="文件名" />
        <el-table-column prop="upload_at" label="上传时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="downloadFile(scope.row)">下载</el-button>
            <el-button size="small" type="danger" @click="deleteFile(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="用户登录" v-model="showLoginModal" width="400px">
      <el-form :model="loginForm" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showLoginModal = false">取消</el-button>
        <el-button type="primary" @click="handleLogin" :loading="loginLoading">登录</el-button>
      </template>
    </el-dialog>

    <el-dialog title="用户注册" v-model="showRegisterModal" width="400px">
      <el-form :model="registerForm" ref="registerFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请再次输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegisterModal = false">取消</el-button>
        <el-button type="primary" @click="handleRegister" :loading="registerLoading">注册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UserFilled, Login, Logout, UserPlus } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const showLoginModal = ref(false)
const showRegisterModal = ref(false)
const loginLoading = ref(false)
const registerLoading = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: ''
})

const userRecords = ref([
  { id: 1, language: 'python', code_content: 'a = [1, 2, 3]\nb = a', created_at: '2024-01-15 10:30:00' },
  { id: 2, language: 'python', code_content: 'x = 42\ny = "hello"', created_at: '2024-01-14 15:20:00' },
  { id: 3, language: 'c', code_content: 'int a = 10;', created_at: '2024-01-13 09:15:00' }
])
const userFiles = ref([
  { id: 1, file_name: 'example.py', upload_at: '2024-01-15 10:30:00' },
  { id: 2, file_name: 'test.c', upload_at: '2024-01-14 14:00:00' }
])

onMounted(() => {
  userStore.initAuth()
})

async function handleLogin() {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  
  loginLoading.value = true
  const success = await userStore.login(loginForm.value.username, loginForm.value.password)
  loginLoading.value = false
  
  if (success) {
    ElMessage.success('登录成功')
    showLoginModal.value = false
    loginForm.value = { username: '', password: '' }
  } else {
    ElMessage.error('登录失败，请检查用户名和密码')
  }
}

async function handleRegister() {
  if (!registerForm.value.username || !registerForm.value.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  
  registerLoading.value = true
  const success = await userStore.register(registerForm.value.username, registerForm.value.password)
  registerLoading.value = false
  
  if (success) {
    ElMessage.success('注册成功，请登录')
    showRegisterModal.value = false
    showLoginModal.value = true
    registerForm.value = { username: '', password: '', confirmPassword: '' }
  } else {
    ElMessage.error('注册失败，用户名可能已存在')
  }
}

function handleLogout() {
  userStore.logout()
  ElMessage.info('已退出登录')
}

function viewRecord(record) {
  router.push({
    path: `/analyze/${record.language === 'python' ? 'python' : 'c'}`,
    state: { code: record.code_content }
  })
}

async function deleteRecord(id) {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userRecords.value = userRecords.value.filter(r => r.id !== id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}

function downloadFile(file) {
  ElMessage.info('下载文件功能开发中')
}

async function deleteFile(id) {
  try {
    await ElMessageBox.confirm('确定要删除这个文件吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userFiles.value = userFiles.value.filter(f => f.id !== id)
    ElMessage.success('删除成功')
  } catch {
    ElMessage.info('已取消删除')
  }
}
</script>

<style scoped>
.user-center {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-info {
  text-align: center;
  padding: 20px 0;
}

.user-name {
  margin-top: 15px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
}
</style>
