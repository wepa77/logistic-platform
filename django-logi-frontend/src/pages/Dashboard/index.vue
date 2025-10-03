<template>
  <div>
    <el-page-header title="Dashboard" content="Overview" class="mb-2" />
    <el-card>
      <p>Welcome, {{ user?.username }} ({{ user?.user_type }})</p>
      <p v-if="user?.balance">Balance: {{ user?.balance }} TMT</p>
      <p v-if="user?.deposit_balance">Deposit: {{ user?.deposit_balance }} TMT</p>
    </el-card>
  </div>
</template>
<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/store/auth'
const auth = useAuthStore(); const { user } = storeToRefs(auth)
</script>
<style scoped>.mb-2{margin-bottom:.75rem}</style>
