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
}
.card {
  width: 400px;
  text-align: center;
}
</style>
