<template>
  <el-container class="app-layout">
    <!-- Sidebar -->
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <img src="@/assets/vue.svg" alt="logo" />
        <span class="brand">Logistic</span>
      </div>

      <!-- ✅ Make sure router prop is here -->
      <el-menu
          router
          :default-active="$route.path"
          background-color="#1f2937"
          text-color="#cbd5e1"
          active-text-color="#409eff"
          class="menu"
      >
        <el-menu-item index="/">
          <i class="mdi mdi-view-dashboard-outline"></i>
          Dashboard
        </el-menu-item>
        <el-menu-item index="/vehicles">
          <i class="mdi mdi-truck"></i> Vehicles
        </el-menu-item>
        <el-menu-item index="/cargos">
          <i class="mdi mdi-package-variant-closed"></i>
          Cargos
        </el-menu-item>
        <el-menu-item index="/offers">
          <i class="mdi mdi-handshake-outline"></i>
          Offers
        </el-menu-item>
        <el-menu-item index="/shipments">
          <i class="mdi mdi-transit-connection-variant"></i>
          Shipments
        </el-menu-item>
        <el-menu-item index="/reviews">
          <i class="mdi mdi-star-outline"></i>
          Reviews
        </el-menu-item>
        <el-menu-item index="/wallet">
          <i class="mdi mdi-wallet-outline"></i>
          Wallet
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- Main content -->
    <el-container>
      <el-header class="header">
        <div class="title">{{ pageTitle }}</div>
        <el-dropdown trigger="click">
          <span class="el-dropdown-link">
            <el-avatar size="small" :src="user?.avatar" />
            <span class="ml-2">{{ user?.username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">Logout</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>

      <el-main class="main">
        <!-- ✅ This is where pages load -->
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const user = computed(() => auth.user)
const pageTitle = computed(() => route.meta.title || 'Dashboard')

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-layout {
  height: 100vh;
}
.sidebar {
  background: #1f2937;
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
}
.logo {
  display: flex;
  align-items: center;
  padding: 1rem;
  color: #fff;
  font-weight: bold;
  font-size: 1.1rem;
}
.logo img {
  width: 28px;
  margin-right: 8px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  padding: 0 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.main {
  background: #f9fafb;
  padding: 20px;
}
</style>
