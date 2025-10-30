<template>
  <div class="onboarding">
    <el-card class="card">
      <h2>Başlaň: rolňy saýlaň</h2>
      <p>Platformada nämäni edýärsiňiz?</p>
      <el-space>
        <el-button type="primary" @click="choose('shipper')">
          <el-icon><Box /></el-icon>
          <span>Men Ýük Ugradýan</span>
        </el-button>
        <el-button type="success" @click="choose('carrier')">
          <el-icon><Van /></el-icon>
          <span>Men Ýük Gatnadýan</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'
import { Box, Van } from '@element-plus/icons-vue'
import { http } from '@/api/http'
import { useRouter } from 'vue-router'

const router = useRouter()
const auth = useAuthStore()

async function choose(type: 'shipper' | 'carrier') {
  try {
    await http.patch('/auth/set-type/', { user_type: type })
    await auth.fetchMe()
    ElMessage.success('Ugradylan!');
    router.push('/') // Dashboard-a ugradyň
  } catch {
    ElMessage.error('Üýtgetmek şowsuz boldy')
  }
}
</script>

<style scoped>
.onboarding {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9fafb;
  padding: 16px; /* ✅ mobile padding */
}

.card {
  width: 400px;
  max-width: 100%; /* ✅ screen-den çykmasyn */
  text-align: center;
  padding: 28px 20px;
  border-radius: 16px;
}

.card h2 {
  font-size: 26px;
  margin-bottom: 12px;
  font-weight: 700;
}

.card p {
  font-size: 16px;
  margin-bottom: 22px;
  color: #64748b;
}

/* Buttons container */
:deep(.el-space) {
  display: flex;
  justify-content: center;
  gap: 16px;
}

/* Desktop buttons */
:deep(.el-button) {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  font-size: 16px;
  border-radius: 10px;
  min-width: 180px;
  justify-content: center;
}

/* ✅ Tablet (max 768px) */
@media (max-width: 768px) {
  .card {
    width: 90%;
    padding: 24px 16px;
  }

  .card h2 {
    font-size: 24px;
  }

  :deep(.el-space) {
    flex-direction: column;
    width: 100%;
  }

  :deep(.el-button) {
    width: 100%;
    min-width: unset;
  }
}

/* ✅ Mobile (max 480px) */
@media (max-width: 480px) {
  .card {
    padding: 20px 14px;
  }

  .card h2 {
    font-size: 22px;
  }

  .card p {
    font-size: 14px;
  }

  :deep(.el-button) {
    font-size: 15px;
    padding: 12px 16px;
  }
}

/* ✅ Mini devices (max 360px) */
@media (max-width: 360px) {
  .card {
    padding: 16px;
  }

  .card h2 {
    font-size: 20px;
  }

  :deep(.el-button) {
    font-size: 14px;
  }
}

</style>
