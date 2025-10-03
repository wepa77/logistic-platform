<script lang="ts" setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'

const username = ref('')
const password = ref('')
const loading = ref(false)
const auth = useAuthStore()   // ✅ Store goşduk

async function handleLogin() {
  loading.value = true
  try {
    await auth.login(username.value, password.value)  // ✅ Store-dan login ulan
    ElMessage.success('Login successful')
    // router.push('/') gerek däl, çünki store.login()-iň içinde bar
  } catch (err) {
    console.error(err)
    ElMessage.error('Login failed. Please check your credentials.')
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <div class="login-header">
<!--        <img src="/logo.png" alt="Logo" class="logo" />-->
        <h2>Logistic Platform</h2>
        <p class="subtitle">Please sign in to continue</p>
      </div>

      <el-form @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="Username">
          <el-input v-model="username" placeholder="Enter username" clearable />
        </el-form-item>

        <el-form-item label="Password">
          <el-input v-model="password" type="password" placeholder="Enter password" clearable show-password />
        </el-form-item>

        <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%; margin-top: 10px"
        >
          Login
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.login-card {
  width: 380px;
  padding: 30px 30px 20px;
  border-radius: 16px;
}

.login-header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 14px;
  margin-top: 4px;
}
</style>
