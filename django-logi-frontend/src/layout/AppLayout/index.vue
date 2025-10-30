<template>
  <el-container class="app-layout">
    <!-- SIDEBAR (hidden after redesign) -->
    <el-aside v-if="false" width="260px" class="sidebar">
        <div class="logo">
          <img :src="logoSrc" alt="Daşa" class="logo-img" />
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
          <el-button
            v-if="isMobile"
            class="menu-toggle"
            text
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <i :class="mobileMenuOpen ? 'mdi mdi-close' : 'mdi mdi-menu'" />
          </el-button>
          <div class="logo-inline">
            <img :src="logoSrc" alt="Daşa" class="logo-img inline" />
          </div>
<!--          <span class="page-title">{{ pageTitle }}</span>-->
        </div>

        <div class="nav-wrap" v-if="!isMobile">
          <el-menu
            mode="horizontal"
            router
            :default-active="$route.path"
            class="top-menu"
            background-color="transparent"
            text-color="var(--el-text-color-primary)"
            active-text-color="var(--el-color-primary)"
          >
            <el-menu-item
              v-for="link in navLinks"
              :key="link.index"
              :index="link.index"
            >
              <i :class="`mdi ${link.icon}`"></i>
              {{ $t(link.labelKey) }}
            </el-menu-item>
          </el-menu>
        </div>

        <div class="header-right">
          <LanguageSwitcher />
          <el-button text class="header-action" :title="isDark ? ($t('common.lightMode') as string) : ($t('common.darkMode') as string)" @click="toggleTheme">
            <i :class="isDark ? 'mdi mdi-white-balance-sunny' : 'mdi mdi-weather-night'"></i>
          </el-button>
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
                <el-dropdown-item @click="$router.push('/profile')">
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

      <el-drawer
        v-model="mobileMenuOpen"
        direction="ltr"
        size="75%"
        class="mobile-drawer"
        :with-header="false"
      >
        <div class="mobile-drawer-inner">
          <div class="mobile-user">
            <el-avatar :size="48" :src="user?.avatar">
              <i class="mdi mdi-account"></i>
            </el-avatar>
            <div class="mobile-user-details">
              <div class="name">{{ user?.username || 'User' }}</div>
              <div class="role">{{ userRole }}</div>
            </div>
          </div>
          <el-menu
            router
            :default-active="$route.path"
            class="mobile-menu"
            background-color="transparent"
            text-color="var(--el-text-color-primary)"
            active-text-color="var(--el-color-primary)"
          >
            <el-menu-item
              v-for="link in navLinks"
              :key="link.index"
              :index="link.index"
              @click="mobileMenuOpen = false"
            >
              <i :class="`mdi ${link.icon}`"></i>
              {{ $t(link.labelKey) }}
            </el-menu-item>
          </el-menu>
          <div class="mobile-actions">
            <el-button type="primary" text @click="toggleTheme">
              <i :class="isDark ? 'mdi mdi-white-balance-sunny' : 'mdi mdi-weather-night'"></i>
              {{ isDark ? $t('common.lightMode') : $t('common.darkMode') }}
            </el-button>
            <el-button type="danger" text @click="logout">
              <i class="mdi mdi-logout"></i>
              {{ $t('nav.logout') }}
            </el-button>
          </div>
        </div>
      </el-drawer>

      <!-- Secondary sub-navigation (ATI-like) -->
      <div class="subnav">
        <div class="subnav-inner" :class="{ 'is-collapsed': isMobile && !mobileSubnavOpen }">
          <router-link to="/cargos" class="subnav-item green">
            <i class="mdi mdi-clipboard-text"></i>
            <span>{{ $t('nav.myCargos') }}</span>
          </router-link>
          <router-link to="/cargos/add" class="subnav-item light-green">
            <i class="mdi mdi-plus-circle-outline"></i>
            <span>{{ $t('nav.addCargo') }}</span>
          </router-link>
          <router-link to="/vehicles" class="subnav-item amber">
            <i class="mdi mdi-truck"></i>
            <span>{{ $t('nav.myVehicles') }}</span>
          </router-link>
          <router-link to="/vehicles/add" class="subnav-item yellow">
            <i class="mdi mdi-plus-circle-outline"></i>
            <span>{{ $t('nav.addVehicle') }}</span>
          </router-link>
          <el-dropdown class="subnav-item orders" trigger="click">
            <span class="el-dropdown-link">
              <i class="mdi mdi-clipboard-check-outline"></i>
              <span>{{ $t('nav.orders') }}</span>
              <i class="mdi mdi-chevron-down small-caret"></i>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/offers')">{{ $t('nav.offers') }}</el-dropdown-item>
                <el-dropdown-item @click="$router.push('/shipments')">{{ $t('nav.shipments') }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
        <el-button
          v-if="isMobile"
          text
          class="subnav-toggle"
          @click="mobileSubnavOpen = !mobileSubnavOpen"
        >
          <span>{{ mobileSubnavOpen ? $t('common.hide') : $t('common.showMore') }}</span>
          <i :class="mobileSubnavOpen ? 'mdi mdi-chevron-up' : 'mdi mdi-chevron-down'"></i>
        </el-button>
      </div>

      <el-main class="main">
        <div v-if="!hideAds" class="ad-banner">
          <el-card class="ad-card" shadow="never">
            <div class="ad-placeholder">{{ $t('common.advertisement') }}</div>
          </el-card>
        </div>
        <template v-if="!hideAds">
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
        </template>
        <template v-else>
          <div class="page-content">
            <router-view />
          </div>
        </template>
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { computed, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { http } from '@/api/http'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const { t } = useI18n()

const user = computed(() => auth.user)
const logoSrc = '/dasha2.png'
const navLinks = [
  { index: '/', icon: 'mdi-home-outline', labelKey: 'nav.home' },
  { index: '/search/cargos', icon: 'mdi-magnify', labelKey: 'nav.searchCargos' },
  { index: '/search/vehicles', icon: 'mdi-magnify', labelKey: 'nav.searchVehicles' },
  { index: '/vehicles', icon: 'mdi-truck', labelKey: 'nav.myVehicles' },
  { index: '/shipments', icon: 'mdi-transit-connection-variant', labelKey: 'nav.shipments' },
  { index: '/cargos', icon: 'mdi-package-variant-closed', labelKey: 'nav.myCargos' },
  { index: '/offers', icon: 'mdi-handshake-outline', labelKey: 'nav.offers' },
  { index: '/driver-request', icon: 'mdi-clipboard-text-outline', labelKey: 'nav.driverRequest' },
  { index: '/reviews', icon: 'mdi-star-outline', labelKey: 'nav.reviews' },
  { index: '/wallet', icon: 'mdi-wallet-outline', labelKey: 'nav.wallet' },
  { index: '/profile', icon: 'mdi-account-circle-outline', labelKey: 'nav.profile' }
]

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
const isMobile = ref(false)
const mobileMenuOpen = ref(false)

// Hide ads in personal cabinet
const hideAds = computed(() => route.name === 'profile')

// THEME: initialize from localStorage or prefers-color-scheme
const THEME_KEY = 'theme'
const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
const isDark = ref((localStorage.getItem(THEME_KEY) || (prefersDark ? 'dark' : 'light')) === 'dark')
applyTheme(isDark.value)

function toggleTheme() {
  isDark.value = !isDark.value
  applyTheme(isDark.value)
  localStorage.setItem(THEME_KEY, isDark.value ? 'dark' : 'light')
}

function applyTheme(dark: boolean) {
  const root = document.documentElement
  if (dark) root.classList.add('dark')
  else root.classList.remove('dark')
}

function updateIsMobile() {
  isMobile.value = window.innerWidth <= 992
  if (!isMobile.value) {
    mobileMenuOpen.value = false
  }
}

// Fetch notifications when component mounts
onMounted(() => {
  updateIsMobile()
  window.addEventListener('resize', updateIsMobile)
})

onMounted(async () => {
  try {
    const { data } = await http.get('/notifications/unread-count/')
    notifications.value = data.count
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateIsMobile)
})

watch(() => route.path, () => {
  mobileMenuOpen.value = false
})

async function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.subnav {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color);
  border-bottom: 1px solid var(--el-border-color);
  justify-content: space-between;
}

.subnav-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.subnav-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 4px;
  color: var(--el-text-color-primary);
  text-decoration: none;
  font-size: 13px;
}
.subnav-item i { font-size: 16px; }
/* keep subtle colored accents; they work in both themes */
.subnav-item.green { background: #d9f99d; color: #111827; }
.subnav-item.light-green { background: #fef08a; color: #111827; }
.subnav-item.amber { background: #e9fac8; color: #111827; }
.subnav-item.yellow { background: #fde68a; color: #111827; }
.subnav-item.orders { padding: 6px 8px; }
.small-caret { font-size: 14px; }
.subnav-toggle {
  display: none;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

/* existing styles */
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
  justify-content: center;
  padding: 1.25rem 1.25rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo-img {
  max-width: 140px;
  width: 100%;
  height: auto;
}

.logo-img.inline {
  max-width: 120px;
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
  background: var(--el-bg-color);
  padding: 0 24px;
  box-shadow: var(--el-box-shadow-light, 0 1px 3px rgba(0,0,0,0.06));
  border-bottom: 1px solid var(--el-border-color);
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
  margin-right: 8px;
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

@media (max-width: 992px) {
  .header {
    padding: 0 16px;
  }

  .nav-wrap {
    display: none;
  }

  .header-left {
    gap: 12px;
  }

  .page-title {
    font-size: 18px;
  }

  .header-right {
    gap: 4px;
  }

  .header-action {
    font-size: 18px;
    padding: 8px;
  }

  .user-dropdown {
    margin-left: 4px;
  }

  .subnav {
    flex-direction: column;
    align-items: stretch;
    gap: 4px;
  }

  .subnav-inner {
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none;
  }

  .subnav-inner::-webkit-scrollbar {
    display: none;
  }

  .subnav-toggle {
    display: inline-flex;
    align-self: flex-end;
  }

  .subnav-inner.is-collapsed {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
  }

  .subnav-inner.is-collapsed .subnav-item {
    opacity: 0;
    pointer-events: none;
  }
}

@media (max-width: 768px) {
  .header {
    flex-wrap: wrap;
    height: auto;
    gap: 12px;
    padding-top: 12px;
    padding-bottom: 12px;
  }

  .header-left {
    width: 100%;
  }

  .header-right {
    width: 100%;
    justify-content: flex-end;
  }

  .main {
    padding: 16px;
    height: auto;
    min-height: calc(100vh - 64px);
  }

  .ad-banner {
    margin-top: 0;
  }
}

@media (max-width: 600px) {
  .page-title {
    font-size: 16px;
  }

  .logo-inline .brand {
    font-size: 16px;
  }

  .header-right {
    gap: 4px;
  }

  .mobile-drawer-inner {
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }

  .mobile-user {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .mobile-user-details .name {
    font-weight: 600;
  }

  .mobile-menu {
    border-right: none;
  }

  .mobile-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: auto;
  }
}

</style>
