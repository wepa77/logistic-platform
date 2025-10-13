<template>
  <div class="dashboard-page">
    <!-- Welcome Section -->
    <div class="welcome-section">
      <div class="welcome-content">
        <div class="welcome-text">
          <h1 class="welcome-title">
            Welcome back, {{ user?.username }}! 👋
          </h1>
          <p class="welcome-subtitle">Here's what's happening with your logistics operations today</p>
        </div>
        <div class="user-badge">
          <el-avatar :size="56" class="user-avatar">
            <i class="mdi mdi-account"></i>
          </el-avatar>
          <div class="user-info">
            <div class="user-name">{{ user?.username }}</div>
            <div class="user-role">{{ formatUserType(user?.user_type) }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Hero Search Section (ATI-style) -->
    <el-card class="search-card" shadow="always">
      <div class="search-grid">
        <div class="field">
          <label>From</label>
          <el-input v-model="search.from" placeholder="City, region, country" />
        </div>
        <div class="field">
          <label>To</label>
          <el-input v-model="search.to" placeholder="City, region, country" />
        </div>
        <div class="field small">
          <label>Radius, km</label>
          <el-input-number v-model="search.radius" :min="0" :max="1000" :step="10" controls-position="right" />
        </div>
        <div class="field small">
          <label>Date</label>
          <el-date-picker v-model="search.date" type="date" placeholder="Select date" style="width: 100%" />
        </div>
        <div class="actions">
          <el-button type="success" size="large" @click="goFind('cargos')">
            <i class="mdi mdi-package-variant"></i> Find Cargos
          </el-button>
          <el-button type="warning" size="large" @click="goFind('vehicles')">
            <i class="mdi mdi-truck"></i> Find Vehicles
          </el-button>
          <el-button size="large" @click="calcDistance">
            <i class="mdi mdi-ruler"></i> Calculate Distance
          </el-button>
        </div>
      </div>
      <div v-if="distanceKm !== null" class="distance-result">
        <i class="mdi mdi-map-marker-distance"></i>
        <span>Distance: {{ distanceKm.toFixed(0) }} km</span>
      </div>
    </el-card>

    <!-- Balance Cards -->
    <div class="balance-grid">
      <div class="balance-card primary">
        <div class="balance-header">
          <div class="balance-icon">
            <i class="mdi mdi-wallet"></i>
          </div>
          <el-button text class="view-btn">
            <i class="mdi mdi-arrow-right"></i>
          </el-button>
        </div>
        <div class="balance-info">
          <div class="balance-label">Current Balance</div>
          <div class="balance-value">{{ formatBalance(user?.balance) }} TMT</div>
        </div>
      </div>

      <div class="balance-card secondary">
        <div class="balance-header">
          <div class="balance-icon">
            <i class="mdi mdi-bank"></i>
          </div>
          <el-button text class="view-btn">
            <i class="mdi mdi-arrow-right"></i>
          </el-button>
        </div>
        <div class="balance-info">
          <div class="balance-label">Deposit Balance</div>
          <div class="balance-value">{{ formatBalance(user?.deposit_balance) }} TMT</div>
        </div>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon cargos">
          <i class="mdi mdi-package-variant-closed"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalCargos }}</div>
          <div class="stat-label">Total Cargos</div>
        </div>
        <div class="stat-trend positive">
          <i class="mdi mdi-trending-up"></i>
          <span>+12%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon vehicles">
          <i class="mdi mdi-truck"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalVehicles }}</div>
          <div class="stat-label">Fleet Vehicles</div>
        </div>
        <div class="stat-trend positive">
          <i class="mdi mdi-trending-up"></i>
          <span>+5%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon shipments">
          <i class="mdi mdi-transit-connection-variant"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalShipments }}</div>
          <div class="stat-label">Active Shipments</div>
        </div>
        <div class="stat-trend neutral">
          <i class="mdi mdi-minus"></i>
          <span>0%</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon offers">
          <i class="mdi mdi-handshake"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalOffers }}</div>
          <div class="stat-label">Pending Offers</div>
        </div>
        <div class="stat-trend positive">
          <i class="mdi mdi-trending-up"></i>
          <span>+8%</span>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="content-grid">
      <!-- Recent Activity -->
      <el-card class="activity-card" shadow="never">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <i class="mdi mdi-history"></i>
              <span>Recent Activity</span>
            </div>
            <el-button text>View All</el-button>
          </div>
        </template>
        <div class="activity-list">
          <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
            <div class="activity-icon" :class="activity.type">
              <i :class="activity.icon"></i>
            </div>
            <div class="activity-content">
              <div class="activity-title">{{ activity.title }}</div>
              <div class="activity-time">{{ activity.time }}</div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- Quick Actions -->
      <el-card class="actions-card" shadow="never">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <i class="mdi mdi-lightning-bolt"></i>
              <span>Quick Actions</span>
            </div>
          </div>
        </template>
        <div class="actions-grid">
          <button class="action-btn" @click="navigateTo('/cargos')">
            <div class="action-icon">
              <i class="mdi mdi-package-variant-closed"></i>
            </div>
            <span>Add Cargo</span>
          </button>
          <button class="action-btn" @click="navigateTo('/vehicles')">
            <div class="action-icon">
              <i class="mdi mdi-truck"></i>
            </div>
            <span>Add Vehicle</span>
          </button>
          <button class="action-btn" @click="navigateTo('/shipments')">
            <div class="action-icon">
              <i class="mdi mdi-transit-connection-variant"></i>
            </div>
            <span>New Shipment</span>
          </button>
          <button class="action-btn" @click="navigateTo('/offers')">
            <div class="action-icon">
              <i class="mdi mdi-handshake"></i>
            </div>
            <span>Create Offer</span>
          </button>
        </div>
      </el-card>
    </div>

    <!-- Bottom Grid -->
    <div class="bottom-grid">
      <!-- Performance Chart -->
      <el-card class="chart-card" shadow="never">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <i class="mdi mdi-chart-line"></i>
              <span>Performance Overview</span>
            </div>
            <el-select v-model="chartPeriod" size="small" style="width: 120px">
              <el-option label="Last 7 days" value="7d" />
              <el-option label="Last 30 days" value="30d" />
              <el-option label="Last 90 days" value="90d" />
            </el-select>
          </div>
        </template>
        <div class="chart-placeholder">
          <i class="mdi mdi-chart-areaspline"></i>
          <p>Performance chart will be displayed here</p>
        </div>
      </el-card>

      <!-- System Status -->
      <el-card class="status-card" shadow="never">
        <template #header>
          <div class="card-header">
            <div class="header-title">
              <i class="mdi mdi-information-outline"></i>
              <span>System Status</span>
            </div>
          </div>
        </template>
        <div class="status-list">
          <div class="status-item">
            <div class="status-indicator online"></div>
            <div class="status-content">
              <div class="status-title">API Services</div>
              <div class="status-value">Operational</div>
            </div>
          </div>
          <div class="status-item">
            <div class="status-indicator online"></div>
            <div class="status-content">
              <div class="status-title">Database</div>
              <div class="status-value">Healthy</div>
            </div>
          </div>
          <div class="status-item">
            <div class="status-indicator online"></div>
            <div class="status-content">
              <div class="status-title">GPS Tracking</div>
              <div class="status-value">Active</div>
            </div>
          </div>
          <div class="status-item">
            <div class="status-indicator warning"></div>
            <div class="status-content">
              <div class="status-title">Payment Gateway</div>
              <div class="status-value">Maintenance</div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import {
  getCargos,
  getVehicles,
  getShipments,
  getOffers
} from '@/api/api'

const auth = useAuthStore()
const { user } = storeToRefs(useAuthStore())
const router = useRouter()

// Stats state
const stats = ref({
  totalCargos: 0,
  totalVehicles: 0,
  totalShipments: 0,
  totalOffers: 0,
})

// Safely format balance values
const formatBalance = (value: number | null | undefined): string => {
  if (value === null || value === undefined) return '0.00'
  return Number(value).toFixed(2)
}

const recentActivities = ref([
  {
    id: 1,
    type: 'cargo',
    icon: 'mdi mdi-package-variant-closed',
    title: 'New cargo added to inventory',
    time: '2 hours ago'
  },
  {
    id: 2,
    type: 'shipment',
    icon: 'mdi mdi-truck-fast',
    title: 'Shipment #1234 delivered successfully',
    time: '5 hours ago'
  },
  {
    id: 3,
    type: 'offer',
    icon: 'mdi mdi-handshake',
    title: 'New offer received from carrier',
    time: '1 day ago'
  },
  {
    id: 4,
    type: 'vehicle',
    icon: 'mdi mdi-truck',
    title: 'Vehicle maintenance completed',
    time: '2 days ago'
  },
])

function formatUserType(type?: string) {
  if (!type) return 'User'
  return type.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

function navigateTo(path: string) {
  router.push(path)
}

// --- Dashboard search panel logic (reused from Marketplace) ---
const search = reactive({ from: '', to: '', radius: 0, date: '' as any })
const distanceKm = ref<number | null>(null)

function goFind(kind: 'cargos' | 'vehicles') {
  router.push({ name: kind, query: {
    from: search.from || undefined,
    to: search.to || undefined,
    radius: search.radius || undefined,
    date: search.date ? new Date(search.date).toISOString().slice(0,10) : undefined
  }})
}

function toRad(d: number) { return (d * Math.PI) / 180 }
function haversineKm(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371
  const dLat = toRad(lat2 - lat1)
  const dLon = toRad(lon2 - lon1)
  const a = Math.sin(dLat/2) ** 2 + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon/2) ** 2
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  return R * c
}

async function geocode(q: string): Promise<{ lat: number; lon: number } | null> {
  if (!q) return null
  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(q)}`
  const res = await fetch(url, { headers: { 'Accept-Language': 'en' } })
  const json = (await res.json()) as Array<{ lat: string; lon: string }> | undefined
  if (!json || !json.length) return null
  const first = json[0] as { lat: string; lon: string }
  return { lat: Number(first.lat), lon: Number(first.lon) }
}

async function calcDistance() {
  distanceKm.value = null
  const [a, b] = await Promise.all([geocode(search.from), geocode(search.to)])
  if (a && b) distanceKm.value = haversineKm(a.lat, a.lon, b.lat, b.lon)
}

async function fetchDashboardData() {
  try {
    const [cargos, vehicles, shipments, offers] = await Promise.all([
      getCargos(),
      getVehicles(),
      getShipments(),
      getOffers()
    ])
    
    stats.value = {
      totalCargos: cargos.data.length,
      totalVehicles: vehicles.data.length,
      totalShipments: shipments.data.length,
      totalOffers: offers.data.length,
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* Welcome Section */
.welcome-section {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 16px;
  padding: 32px;
  color: white;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.welcome-text {
  flex: 1;
}

.welcome-title {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: white;
}

.welcome-subtitle {
  font-size: 16px;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.15);
  padding: 16px 24px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.user-avatar {
  background: rgba(255, 255, 255, 0.2);
  font-size: 28px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.user-role {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}

/* Balance Cards */
.balance-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.balance-card {
  border-radius: 16px;
  padding: 24px;
  color: white;
  transition: all 0.3s ease;
}

.balance-card.primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
}

.balance-card.secondary {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.balance-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.balance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.balance-icon {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.view-btn {
  color: white;
  font-size: 20px;
}

.balance-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.balance-label {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.balance-value {
  font-size: 36px;
  font-weight: 700;
  color: white;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-icon.cargos {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.vehicles {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.shipments {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.offers {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  font-weight: 500;
}

.stat-trend {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
}

.stat-trend.positive {
  color: #10b981;
  background: #d1fae5;
}

.stat-trend.neutral {
  color: #64748b;
  background: #f1f5f9;
}

.stat-trend i {
  font-size: 14px;
}

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.activity-card,
.actions-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}

.header-title i {
  color: #3b82f6;
  font-size: 20px;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background: #f8fafc;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.activity-icon.cargo {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.activity-icon.shipment {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.activity-icon.offer {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.activity-icon.vehicle {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #94a3b8;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.action-btn:hover {
  border-color: #3b82f6;
  background: #eff6ff;
  transform: translateY(-2px);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
}

/* Bottom Grid */
.bottom-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.chart-card,
.status-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #cbd5e1;
}

.chart-placeholder i {
  font-size: 64px;
  margin-bottom: 16px;
}

.chart-placeholder p {
  font-size: 14px;
  margin: 0;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  background: #f8fafc;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-indicator.online {
  background: #10b981;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2);
}

.status-indicator.warning {
  background: #f59e0b;
  box-shadow: 0 0 0 4px rgba(245, 158, 11, 0.2);
}

.status-content {
  flex: 1;
}

.status-title {
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
  margin-bottom: 2px;
}

.status-value {
  font-size: 12px;
  color: #64748b;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .bottom-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .welcome-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
.search-card { margin: 16px 0 24px; border-radius: 14px; }
.search-grid { display: grid; grid-template-columns: 1fr 1fr 160px 220px; gap: 16px; align-items: end; }
.field label { display: block; font-size: 12px; color: #64748b; margin-bottom: 6px; }
.field.small { min-width: 140px; }
.actions { display: flex; gap: 12px; align-items: center; }
.distance-result { margin-top: 12px; color: #334155; display: flex; align-items: center; gap: 8px; }
@media (max-width: 1024px) { .search-grid { grid-template-columns: 1fr 1fr; } .actions { grid-column: 1 / -1; } }

</style>
