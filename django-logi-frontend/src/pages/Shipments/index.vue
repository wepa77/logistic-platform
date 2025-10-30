<template>
  <div class="shipments-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-transit-connection-variant"></i>
            Shipments Management
          </h1>
          <p class="page-subtitle">Track and manage all shipment operations</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" size="large" @click="openDialog()" class="add-btn">
            <i class="mdi mdi-plus"></i>
            Create Shipment
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            placeholder="Search by cargo, carrier..."
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="paymentFilter" placeholder="Payment Status" clearable class="payment-filter">
          <el-option label="All Status" value="" />
          <el-option label="Paid" value="paid" />
          <el-option label="Pending" value="pending" />
          <el-option label="Failed" value="failed" />
        </el-select>

        <el-button class="filter-btn" @click="fetchShipments">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-package-variant-closed"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ shipments.length }}</div>
          <div class="stat-label">Total Shipments</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon paid">
          <i class="mdi mdi-check-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.paid }}</div>
          <div class="stat-label">Paid</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pending">
          <i class="mdi mdi-clock-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-label">Pending</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon revenue">
          <i class="mdi mdi-cash-multiple"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalRevenue.toFixed(2) }}</div>
          <div class="stat-label">Total Revenue (TMT)</div>
        </div>
      </div>
    </div>

    <!-- Shipments Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredShipments" style="width: 100%" class="modern-table">
        <el-table-column label="Cargo" min-width="200">
          <template #default="{ row }">
            <div class="cargo-cell">
              <i class="mdi mdi-package-variant-closed"></i>
              <span>{{ row.cargo?.title || 'N/A' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Carrier" min-width="180">
          <template #default="{ row }">
            <div class="carrier-cell">
              <el-avatar :size="32" class="carrier-avatar">
                <i class="mdi mdi-account"></i>
              </el-avatar>
              <span>{{ row.carrier?.username || 'N/A' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Details" min-width="200">
          <template #default="{ row }">
            <div class="details-cell">
              <div class="detail-item">
                <i class="mdi mdi-map-marker-distance"></i>
                <span>{{ row.distance_km || 0 }} km</span>
              </div>
              <div class="detail-item">
                <i class="mdi mdi-cash"></i>
                <span>{{ row.total_price || 0 }} TMT</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Commission" width="140">
          <template #default="{ row }">
            <div class="commission-cell">
              <i class="mdi mdi-percent"></i>
              <span>{{ row.commission_amount || 0 }} TMT</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Payment" width="140">
          <template #default="{ row }">
            <el-tag
                :type="paymentTagType(row.payment_status)"
                :class="`payment-tag payment-${row.payment_status}`"
                effect="plain"
            >
              <i :class="paymentIcon(row.payment_status)"></i>
              {{ formatPaymentStatus(row.payment_status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Timeline" min-width="180">
          <template #default="{ row }">
            <div class="timeline-cell">
              <div class="time-item" v-if="row.start_time">
                <i class="mdi mdi-clock-start"></i>
                <span>{{ formatTime(row.start_time) }}</span>
              </div>
              <div class="time-item" v-if="row.end_time">
                <i class="mdi mdi-clock-end"></i>
                <span>{{ formatTime(row.end_time) }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Actions" width="160">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-tooltip content="Edit" placement="top">
                <el-button link type="primary" @click="openDialog(row)">
                  <i class="mdi mdi-pencil"></i>
                </el-button>
              </el-tooltip>
              <el-tooltip content="View Details" placement="top">
                <el-button link type="info">
                  <i class="mdi mdi-eye"></i>
                </el-button>
              </el-tooltip>
              <el-popconfirm
                  title="Are you sure to delete this shipment?"
                  @confirm="deleteShipment(row.id!)"
              >
                <template #reference>
                  <el-tooltip content="Delete" placement="top">
                    <el-button link type="danger">
                      <i class="mdi mdi-delete"></i>
                    </el-button>
                  </el-tooltip>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Modern Dialog for create/update -->
    <el-dialog
        v-model="dialogVisible"
        :title="form.id ? 'Edit Shipment' : 'Create New Shipment'"
        width="700px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="shipment-form">
        <div class="form-grid">
          <el-form-item label="Cargo" class="form-item-full">
            <el-select v-model="form.cargo" placeholder="Select cargo" filterable style="width:100%">
              <el-option
                  v-for="c in cargoOptions"
                  :key="c.id"
                  :label="c.title"
                  :value="c.id"
              >
                <div class="option-item">
                  <i class="mdi mdi-package-variant-closed"></i>
                  <span>{{ c.title }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Carrier" class="form-item-full">
            <el-select v-model="form.carrier" placeholder="Select carrier" filterable style="width:100%">
              <el-option
                  v-for="u in carrierOptions"
                  :key="u.id"
                  :label="u.username"
                  :value="u.id"
              >
                <div class="option-item">
                  <i class="mdi mdi-account"></i>
                  <span>{{ u.username }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Vehicle (Optional)" class="form-item-full">
            <el-select v-model="form.vehicle" placeholder="Select vehicle" filterable clearable style="width:100%">
              <el-option
                  v-for="v in vehicleOptions"
                  :key="v.id"
                  :label="`${v.plate_number} - ${v.brand} ${v.model} (${v.capacity_kg}kg)`"
                  :value="v.id"
              >
                <div class="option-item">
                  <i class="mdi mdi-truck"></i>
                  <span>{{ v.plate_number }} - {{ v.brand }} {{ v.model }} ({{ v.capacity_kg }}kg)</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="Distance (km)">
            <el-input-number v-model="form.distance_km" :min="0" :step="1" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Total Price (TMT)">
            <el-input-number v-model="form.total_price" :min="0" :step="10" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Payment Status" class="form-item-full">
            <el-select v-model="form.payment_status" placeholder="Select status" style="width: 100%">
              <el-option label="Paid" value="paid">
                <div class="option-item">
                  <i class="mdi mdi-check-circle"></i>
                  <span>Paid</span>
                </div>
              </el-option>
              <el-option label="Pending" value="pending">
                <div class="option-item">
                  <i class="mdi mdi-clock-outline"></i>
                  <span>Pending</span>
                </div>
              </el-option>
              <el-option label="Failed" value="failed">
                <div class="option-item">
                  <i class="mdi mdi-close-circle"></i>
                  <span>Failed</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button size="large" @click="dialogVisible = false">
            <i class="mdi mdi-close"></i>
            Cancel
          </el-button>
          <el-button type="primary" size="large" @click="saveShipment">
            <i class="mdi mdi-check"></i>
            {{ form.id ? 'Update' : 'Create' }} Shipment
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  getShipments as apiGetShipments,
  createShipment as apiCreateShipment,
  updateShipment as apiUpdateShipment,
  deleteShipment as apiDeleteShipment,
  getCargos as apiGetCargos,
  getUsers as apiGetUsers,
  getVehicles as apiGetVehicles
} from '@/api/api'

interface Shipment {
  id?: number
  cargo: any
  carrier: any
  vehicle: number | null
  distance_km: number | null
  total_price: number | null
  payment_status: string
  commission_amount?: number
  start_time?: string
  end_time?: string
}

const shipments = ref<Shipment[]>([])
const cargoOptions = ref<any[]>([])
const carrierOptions = ref<any[]>([])
const vehicleOptions = ref<any[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const paymentFilter = ref('')

const form = ref<Shipment>({
  cargo: null,
  carrier: null,
  vehicle: null,
  distance_km: null,
  total_price: null,
  payment_status: 'pending'
})

// Computed stats
const stats = computed(() => {
  return {
    paid: shipments.value.filter(s => s.payment_status === 'paid').length,
    pending: shipments.value.filter(s => s.payment_status === 'pending').length,
    totalRevenue: shipments.value
      .filter(s => s.payment_status === 'paid')
      .reduce((sum, s) => sum + (s.commission_amount || 0), 0),
  }
})

// Filtered shipments
const filteredShipments = computed(() => {
  let filtered = shipments.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(shipment =>
      shipment.cargo?.title?.toLowerCase().includes(query) ||
      shipment.carrier?.username?.toLowerCase().includes(query)
    )
  }

  // Filter by payment status
  if (paymentFilter.value) {
    filtered = filtered.filter(shipment => shipment.payment_status === paymentFilter.value)
  }

  return filtered
})

async function fetchShipments() {
  const { data } = await apiGetShipments()
  shipments.value = data
}

async function fetchOptions() {
  const { data: cargos } = await apiGetCargos()
  cargoOptions.value = cargos

  const { data: users } = await apiGetUsers({ user_type: 'carrier' })
  carrierOptions.value = users

  const { data: vehicles } = await apiGetVehicles()
  vehicleOptions.value = vehicles
}

function openDialog(shipment?: Shipment) {
  if (shipment) {
    form.value = {
      ...shipment,
      cargo: shipment.cargo?.id || shipment.cargo,
      carrier: shipment.carrier?.id || shipment.carrier
    }
  } else {
    form.value = {
      cargo: null,
      carrier: null,
      vehicle: null,
      distance_km: null,
      total_price: null,
      payment_status: 'pending'
    }
  }
  dialogVisible.value = true
}

async function saveShipment() {
  if (form.value.id) {
    await apiUpdateShipment(form.value.id, form.value)
    ElMessage.success('Shipment updated successfully')
  } else {
    await apiCreateShipment(form.value)
    ElMessage.success('Shipment created successfully')
  }
  dialogVisible.value = false
  await fetchShipments()
}

async function deleteShipment(id: number) {
  await apiDeleteShipment(id)
  ElMessage.success('Shipment deleted successfully')
  await fetchShipments()
}

function paymentTagType(status: string) {
  switch (status) {
    case 'paid': return 'success'
    case 'pending': return 'warning'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

function paymentIcon(status: string) {
  switch (status) {
    case 'paid': return 'mdi mdi-check-circle'
    case 'pending': return 'mdi mdi-clock-outline'
    case 'failed': return 'mdi mdi-close-circle'
    default: return 'mdi mdi-help-circle'
  }
}

function formatPaymentStatus(status: string) {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

function formatTime(time: string) {
  if (!time) return 'N/A'
  return new Date(time).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await fetchOptions()
  await fetchShipments()
})
</script>

<style scoped>
/* ==========================================================
 ✅ Responsive Enhancements for Shipments Management Page
========================================================== */

/* ---------- 1280px ↓ ---------- */
@media (max-width: 1280px) {
  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* ---------- 1024px ↓ Tablets ---------- */
@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .filters-container {
    flex-wrap: wrap;
    gap: 10px;
  }

  .search-input {
    flex: 1 1 100%;
    max-width: none;
  }

  .payment-filter {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-grid {
    grid-template-columns: 1fr 1fr;
  }
}

/* ---------- 768px ↓ Mobile / Small tablets ---------- */
@media (max-width: 768px) {

  .page-title {
    font-size: 22px;
  }

  .page-subtitle {
    font-size: 13px;
  }

  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input,
  .payment-filter {
    width: 100%;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  /* ✅ Table must scroll horizontally */
  .table-card {
    overflow-x: auto;
  }

  .modern-table :deep(.el-table__body-wrapper) {
    overflow-x: auto;
  }

  /* ✅ Form grid becomes 1 column */
  .form-grid {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .add-btn {
    width: 100%;
  }
}

/* ---------- 600px ↓ Phones ---------- */
@media (max-width: 600px) {
  .shipments-page {
    padding: 10px;
  }

  .page-title {
    font-size: 20px;
  }

  .stat-card {
    padding: 14px;
  }

  .stat-value {
    font-size: 22px;
  }

  .filters-card {
    padding: 12px;
  }

  .details-cell {
    gap: 4px;
  }
}

/* ---------- 480px ↓ Small phones ---------- */
@media (max-width: 480px) {

  .page-title {
    font-size: 18px;
  }

  .add-btn {
    padding: 10px 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-card {
    padding: 12px;
  }

  .filters-container {
    gap: 8px;
  }

  .dialog-footer {
    flex-direction: column;
    gap: 8px;
  }

  .dialog-footer .el-button {
    width: 100%;
  }
}

/* ---------- 360px ↓ Ultra-small ---------- */
@media (max-width: 360px) {

  .page-title {
    font-size: 16px;
  }

  .page-subtitle {
    font-size: 12px;
  }

  .filters-card {
    padding: 8px;
  }

  .stat-card {
    padding: 10px;
  }

  .form-grid {
    gap: 10px;
  }
}

</style>
