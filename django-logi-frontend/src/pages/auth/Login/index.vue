<template>
  <div class="auth-container">
    <div class="language-switcher-wrapper">
      <LanguageSwitcher />
    </div>
    <el-card class="auth-card" shadow="always">
      <h2 class="auth-title">{{ $t('auth.login') }}</h2>
      <el-form @submit.prevent="handleLogin" label-position="top">
        <el-form-item :label="$t('auth.username')">
          <el-input v-model="username" :placeholder="$t('auth.username')" clearable />
        </el-form-item>

        <el-form-item :label="$t('auth.password')">
          <el-input v-model="password" type="password" :placeholder="$t('auth.password')" clearable show-password />
        </el-form-item>

        <div class="auth-actions">
          <el-checkbox v-model="remember">{{ $t('auth.rememberMe') }}</el-checkbox>
          <router-link to="/forgot" class="forgot">{{ $t('auth.forgotPassword') }}</router-link>
        </div>

        <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            style="width: 100%; margin-top: 10px"
        >
          {{ $t('auth.signIn') }}
        </el-button>
      </el-form>

      <div class="register">
        {{ $t('auth.dontHaveAccount') }}
        <router-link to="/register">{{ $t('auth.signUp') }}</router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

const { t } = useI18n()
const username = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function handleLogin() {
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    ElMessage.success(t('dashboard.welcomeBack') + '!')
    router.push('/')
  } catch (err) {
    console.error(err)
    ElMessage.error(t('messages.operationFailed'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  position: relative;
}

.language-switcher-wrapper {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
  background: white;
  padding: 8px 12px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.auth-card {
  width: 380px;
  padding: 30px;
  border-radius: 16px;
}
.auth-title {
  text-align: center;
  margin-bottom: 20px;
}
.auth-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.forgot {
  font-size: 13px;
  color: #2563eb;
  text-decoration: underline;
}
.register {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
}
</style>
