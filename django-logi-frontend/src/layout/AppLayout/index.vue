<template>
  <el-container class="app-layout">
    <!-- SIDEBAR (hidden after redesign) -->
    <el-aside v-if="false" width="260px" class="sidebar">
      <div class="logo">
        <div class="logo-icon">
          <i class="mdi mdi-truck-fast"></i>
        </div>
        <span class="brand">Logistic</span>
      </div>

      <!-- MENU -->
      <el-menu
          router
          :default-active="$route.path"
          background-color="transparent"
          text-color="#94a3b8"
          active-text-color="#fff"
          class="menu"
      >
        <el-menu-item index="/">
          <i class="mdi mdi-home-outline menu-icon"></i>
          <span>{{ $t('nav.home') }}</span>
        </el-menu-item>

        <!-- Carrier & Shipper menus: visible to all authenticated users to avoid backend role mismatch -->
        <el-menu-item index="/vehicles">
          <i class="mdi mdi-truck menu-icon"></i>
          <span>{{ $t('nav.vehicles') }}</span>
        </el-menu-item>
        <el-menu-item index="/shipments">
          <i class="mdi mdi-transit-connection-variant menu-icon"></i>
          <span>{{ $t('nav.shipments') }}</span>
        </el-menu-item>

        <el-menu-item index="/cargos">
          <i class="mdi mdi-package-variant-closed menu-icon"></i>
          <span>{{ $t('nav.cargos') }}</span>
        </el-menu-item>
        <el-menu-item index="/offers">
          <i class="mdi mdi-handshake-outline menu-icon"></i>
          <span>{{ $t('nav.offers') }}</span>
        </el-menu-item>

        <!-- Common -->
        <el-menu-item index="/driver-request">
          <i class="mdi mdi-clipboard-text-outline menu-icon"></i>
          <span>{{ $t('nav.driverRequest') }}</span>
        </el-menu-item>
        <el-menu-item index="/reviews">
          <i class="mdi mdi-star-outline menu-icon"></i>
          <span>{{ $t('nav.reviews') }}</span>
        </el-menu-item>
        <el-menu-item index="/wallet">
          <i class="mdi mdi-wallet-outline menu-icon"></i>
          <span>{{ $t('nav.wallet') }}</span>
        </el-menu-item>
      </el-menu>

      <!-- USER FOOTER -->
      <div class="sidebar-footer">
        <el-avatar :size="40" :src="user?.avatar" class="user-avatar">
          <i class="mdi mdi-account"></i>
        </el-avatar>
        <div class="user-details">
          <div class="user-name">{{ user?.username || 'User' }}</div>
          <div class="user-role">{{ userRole }}</div>
        </div>
      </div>
    </el-aside>

    <!-- MAIN -->
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <div class="logo-inline">
            <div class="logo-icon small"><i class="mdi mdi-truck-fast"></i></div>
            <span class="brand">Logistic</span>
          </div>
          <span class="page-title">{{ pageTitle }}</span>
        </div>

        <div class="nav-wrap">
          <el-menu
            mode="horizontal"
            router
            :default-active="$route.path"
            class="top-menu"
            background-color="transparent"
            text-color="#334155"
            active-text-color="#111827"
          >
            <el-menu-item index="/"><i class="mdi mdi-home-outline"></i> {{ $t('nav.home') }}</el-menu-item>
            <el-menu-item index="/vehicles"><i class="mdi mdi-truck"></i> {{ $t('nav.vehicles') }}</el-menu-item>
            <el-menu-item index="/shipments"><i class="mdi mdi-transit-connection-variant"></i> {{ $t('nav.shipments') }}</el-menu-item>
            <el-menu-item index="/cargos"><i class="mdi mdi-package-variant-closed"></i> {{ $t('nav.cargos') }}</el-menu-item>
            <el-menu-item index="/offers"><i class="mdi mdi-handshake-outline"></i> {{ $t('nav.offers') }}</el-menu-item>
            <el-menu-item index="/driver-request"><i class="mdi mdi-clipboard-text-outline"></i> {{ $t('nav.driverRequest') }}</el-menu-item>
            <el-menu-item index="/reviews"><i class="mdi mdi-star-outline"></i> {{ $t('nav.reviews') }}</el-menu-item>
            <el-menu-item index="/wallet"><i class="mdi mdi-wallet-outline"></i> {{ $t('nav.wallet') }}</el-menu-item>
          </el-menu>
        </div>

        <div class="header-right">
          <LanguageSwitcher />
          <el-button text class="header-action">
            <i class="mdi mdi-bell-outline"></i>
            <span v-if="notifications>0" class="notification-badge">{{ notifications }}</span>
          </el-button>
          <el-dropdown trigger="click" class="user-dropdown">
            <div class="user-trigger">
              <el-avatar :size="36" :src="user?.avatar">
                <i class="mdi mdi-account"></i>
              </el-avatar>
              <i class="mdi mdi-chevron-down"></i>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>
                  <i class="mdi mdi-account-outline"></i> {{ $t('nav.profile') }}
                </el-dropdown-item>
                <el-dropdown-item>
                  <i class="mdi mdi-cog-outline"></i> {{ $t('nav.settings') }}
                </el-dropdown-item>
                <el-dropdown-item divided @click="logout">
                  <i class="mdi mdi-logout"></i> {{ $t('nav.logout') }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main">
        <div class="ad-banner">
          <el-card class="ad-card" shadow="never">
            <div class="ad-placeholder">{{ $t('common.advertisement') }}</div>
          </el-card>
        </div>
        <div class="content-with-ads">
          <aside class="ad-rail">
            <el-card class="ad-rail-card" shadow="never">
              <div class="ad-rail-placeholder">{{ $t('common.adShort') }}</div>
            </el-card>
          </aside>
          <div class="page-content">
            <router-view />
          </div>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { computed, ref, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRoute, useRouter } from 'vue-router'
import { http } from '@/api/http'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const user = computed(() => auth.user)
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const userRole = computed(() => {
  if (auth.isCarrier) return t('userTypes.carrier')
  if (auth.isShipper) return t('userTypes.cargo_owner')
  return t('userTypes.user')
})

const pageTitle = computed(() => {
  // Prefer nav.* translation by route name if available, else fallback to meta title
  const name = route.name as string | undefined
  if (name) {
    const key = `nav.${name}`
    const translated = t(key)
    if (translated !== key) return translated
  }
  return (route.meta.title as string) || t('nav.home')
})
const notifications = ref(0)

// Fetch notifications when component mounts
onMounted(async () => {
  try {
    const { data } = await http.get('/notifications/unread-count/')
    notifications.value = data.count
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  }
})

async function logout() {
  auth.logout()
  router.push('/login')
}
</script>


<style scoped>
.app-layout {
  height: 100vh;
  overflow: hidden;
}

/* Sidebar Styles */
.sidebar {
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.logo {
  display: flex;
  align-items: center;
  padding: 1.5rem 1.25rem;
  color: #fff;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.brand {
  font-weight: 700;
  font-size: 1.35rem;
  letter-spacing: -0.5px;
}

.menu {
  flex-grow: 1;
  border-right: none;
  padding: 1rem 0.75rem;
  overflow-y: auto;
}

.menu :deep(.el-menu-item) {
  border-radius: 10px;
  margin-bottom: 6px;
  padding: 0 16px;
  height: 48px;
  line-height: 48px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.menu :deep(.el-menu-item:hover) {
  background: rgba(59, 130, 246, 0.1) !important;
  color: #60a5fa !important;
}

.menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.menu-icon {
  font-size: 20px;
  margin-right: 12px;
  width: 20px;
  display: inline-block;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(0, 0, 0, 0.2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.05);
}

.user-avatar {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.user-details {
  flex: 1;
  overflow: hidden;
}

.user-name {
  font-weight: 600;
  font-size: 14px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
}

/* Header Styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  padding: 0 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  border-bottom: 1px solid #f1f5f9;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-toggle {
  font-size: 24px;
  color: #64748b;
  padding: 8px;
  transition: all 0.3s ease;
}

.menu-toggle:hover {
  color: #3b82f6;
  background: #f1f5f9;
  border-radius: 8px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #0f172a;
  letter-spacing: -0.3px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-action {
  position: relative;
  font-size: 20px;
  color: #64748b;
  padding: 10px;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.header-action:hover {
  color: #3b82f6;
  background: #f1f5f9;
}

.notification-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 5px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.user-dropdown {
  margin-left: 8px;
}

.user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-trigger:hover {
  background: #f1f5f9;
}

.user-trigger i {
  color: #94a3b8;
  font-size: 18px;
}

/* Main Content */
.main {
  background: #f8fafc;
  padding: 24px;
  overflow-y: auto;
  height: calc(100vh - 64px);
}

/* Scrollbar Styling */
.menu::-webkit-scrollbar {
  width: 6px;
}

.menu::-webkit-scrollbar-track {
  background: transparent;
}

.menu::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.menu::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

.main::-webkit-scrollbar {
  width: 8px;
}

.main::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.main::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.main::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
.top-menu :deep(.el-menu-item) { padding: 0 12px; }
.top-menu :deep(.el-menu-item i) { margin-right: 6px; }
.nav-wrap { flex: 1; display: flex; justify-content: center; }
.logo-inline { display: flex; align-items: center; gap: 8px; }
.logo-icon.small { width: 28px; height: 28px; font-size: 18px; }

/* Ad areas */
.ad-banner { margin: 12px 0 16px; }
.ad-placeholder { height: 64px; display: grid; place-items: center; color: #334155; background: #f1f5f9; border: 1px dashed #cbd5e1; border-radius: 8px; }

.content-with-ads { display: grid; grid-template-columns: 300px 1fr; gap: 16px; }
.ad-rail-placeholder { height: 520px; display: grid; place-items: center; color: #334155; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; }
.page-content { min-width: 0; }

@media (max-width: 1024px) {
  .content-with-ads { grid-template-columns: 1fr; }
  .ad-rail { display: none; }
}

</style>
