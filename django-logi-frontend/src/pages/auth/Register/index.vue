<template>
  <div class="auth-container">
    <div class="language-switcher-wrapper">
      <LanguageSwitcher />
    </div>
    <el-card class="auth-card" shadow="always">
      <h2 class="auth-title">{{ $t('auth.registrationTitle') }}</h2>
      
      <!-- Step 1: Role Selection -->
      <div v-if="!selectedRole" class="role-selection">
        <div class="profile-section">
          <h3 class="section-title">{{ $t('auth.selectProfile') }}</h3>
          <p class="section-description">
            {{ $t('auth.profileDescription') }}
          </p>
        </div>

        <div class="role-options">
          <div 
            class="role-card" 
            @click="selectRole('carrier')"
          >
            <div class="role-content">
              <div class="role-info">
                <div class="role-title">{{ $t('auth.carrier') }}</div>
                <div class="role-description">{{ $t('auth.carrierDescription') }}</div>
              </div>
              <el-icon class="role-arrow"><ArrowRight /></el-icon>
            </div>
          </div>

          <div 
            class="role-card" 
            @click="selectRole('forwarder')"
          >
            <div class="role-content">
              <div class="role-info">
                <div class="role-title">{{ $t('auth.forwarder') }}</div>
                <div class="role-description">{{ $t('auth.forwarderDescription') }}</div>
              </div>
              <el-icon class="role-arrow"><ArrowRight /></el-icon>
            </div>
          </div>

          <div 
            class="role-card" 
            @click="selectRole('cargo_owner')"
          >
            <div class="role-content">
              <div class="role-info">
                <div class="role-title">{{ $t('auth.cargoOwner') }}</div>
                <div class="role-description">{{ $t('auth.cargoOwnerDescription') }}</div>
              </div>
              <el-icon class="role-arrow"><ArrowRight /></el-icon>
            </div>
          </div>
        </div>

        <el-button
          type="default"
          size="large"
          class="show-more-btn"
        >
          {{ $t('auth.showMore') }}
        </el-button>

        <div class="login-link">
          <router-link to="/login">{{ $t('auth.alreadyHaveAccount') }}</router-link>
        </div>
      </div>

      <!-- Step 2: Registration Form -->
      <div v-else class="registration-form">
        <div class="back-button" @click="selectedRole = ''">
          <el-icon><ArrowLeft /></el-icon>
          <span>{{ getRoleLabel(selectedRole) }}</span>
        </div>

        <el-form @submit.prevent="handleRegister" label-position="top">
          <el-form-item :label="$t('auth.email')">
            <el-input 
              v-model="formData.email" 
              type="email"
              clearable 
            />
          </el-form-item>

          <el-form-item :label="$t('auth.login')">
            <el-input 
              v-model="formData.username" 
              clearable 
            />
          </el-form-item>

          <el-form-item :label="$t('auth.password')">
            <el-input 
              v-model="formData.password" 
              type="password" 
              show-password 
            />
          </el-form-item>

          <el-form-item :label="$t('auth.phone')">
            <div class="phone-input-wrapper">
              <el-select v-model="phoneCode" class="phone-code-select">
                <el-option label="🇹🇲 +993" value="+993" />
                <el-option label="🇷🇺 +7" value="+7" />
                <el-option label="🇺🇸 +1" value="+1" />
              </el-select>
              <el-input 
                v-model="formData.phone" 
                class="phone-number-input"
                placeholder="65 123456"
              />
            </div>
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="agreeToTerms">
              {{ $t('auth.agreeToTerms') }}
            </el-checkbox>
          </el-form-item>

          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleRegister"
            style="width: 100%"
          >
            {{ $t('auth.continue') }}
          </el-button>
        </el-form>

        <div class="terms-notice">
          {{ $t('auth.termsNotice') }}
          <a href="#" class="terms-link">{{ $t('auth.userAgreement') }}</a>
        </div>

        <div class="login-link">
          <router-link to="/login">{{ $t('auth.alreadyHaveAccount') }}</router-link>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { ArrowRight, ArrowLeft } from '@element-plus/icons-vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { http } from '@/api/http'

const { t } = useI18n()
const selectedRole = ref('')
const router = useRouter()
const loading = ref(false)
const agreeToTerms = ref(false)
const phoneCode = ref('+993')

const formData = ref({
  email: '',
  username: '',
  password: '',
  phone: ''
})

function selectRole(role: string) {
  selectedRole.value = role
}

function getRoleLabel(role: string) {
  const labels: Record<string, string> = {
    carrier: t('auth.carrier'),
    forwarder: t('auth.forwarder'),
    cargo_owner: t('auth.cargoOwner')
  }
  return labels[role] || role
}

async function handleRegister() {
  if (!formData.value.email || !formData.value.username || !formData.value.password || !formData.value.phone) {
    ElMessage.warning(t('messages.required'))
    return
  }

  loading.value = true
  try {
    await http.post('/auth/register/', {
      email: formData.value.email,
      username: formData.value.username,
      password: formData.value.password,
      phone: phoneCode.value + formData.value.phone,
      user_type: selectedRole.value
    })
    ElMessage.success(t('messages.operationSuccess'))
    router.push('/login')
  } catch (err: any) {
    console.error(err)
    ElMessage.error(err.response?.data?.message || t('messages.operationFailed'))
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
  background: #f5f5f5;
  padding: 20px;
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
  width: 100%;
  max-width: 500px;
  padding: 40px;
  border-radius: 20px;
}

.auth-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 30px;
  color: #1a1a1a;
}

.profile-section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #1a1a1a;
}

.section-description {
  font-size: 14px;
  line-height: 1.6;
  color: #666;
  margin: 0;
}

.role-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.role-card {
  background: #f8f8f8;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 18px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.role-card:hover {
  background: #f0f0f0;
}

.role-card.selected {
  background: #fff;
  border-color: #3b82f6;
}

.role-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.role-info {
  flex: 1;
}

.role-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 6px;
}

.role-description {
  font-size: 13px;
  color: #888;
  line-height: 1.4;
}

.role-arrow {
  font-size: 20px;
  color: #999;
  margin-left: 12px;
}

.show-more-btn {
  width: 100%;
  margin-bottom: 16px;
  height: 44px;
  font-size: 15px;
  background: #e8e8e8;
  border: none;
  color: #1a1a1a;
}

.show-more-btn:hover {
  background: #d8d8d8;
}

.login-link {
  text-align: center;
  font-size: 14px;
}

.login-link a {
  color: #3b82f6;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

/* Registration Form Styles */
.registration-form {
  margin-top: 20px;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #fef3c7;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 24px;
  font-size: 15px;
  font-weight: 500;
  color: #1a1a1a;
  transition: background 0.2s;
}

.back-button:hover {
  background: #fde68a;
}

.back-button .el-icon {
  font-size: 18px;
}

.registration-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.registration-form :deep(.el-input__inner) {
  height: 44px;
  border-radius: 8px;
}

.phone-input-wrapper {
  display: flex;
  gap: 8px;
  width: 100%;
  align-items: stretch;
}

.phone-code-select {
  width: 120px;
  flex-shrink: 0;
}

.phone-code-select :deep(.el-input__wrapper) {
  height: 44px;
  border-radius: 8px;
}

.phone-code-select :deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  border-radius: 8px;
}

.phone-number-input {
  flex: 1;
}

.phone-number-input :deep(.el-input__wrapper) {
  height: 44px;
  border-radius: 8px;
}

.phone-number-input :deep(.el-input__inner) {
  height: 44px;
  line-height: 44px;
  border-radius: 8px;
}

.registration-form :deep(.el-checkbox) {
  font-size: 14px;
  color: #666;
}

.registration-form :deep(.el-button--primary) {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  margin-top: 8px;
}

.terms-notice {
  text-align: center;
  font-size: 13px;
  color: #666;
  margin-top: 16px;
  line-height: 1.5;
}

.terms-link {
  color: #3b82f6;
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}
</style>
