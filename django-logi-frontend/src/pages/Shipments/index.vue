<template>
  <div class="shipments-page">
    <div class="page-hero">
      <div class="hero-info">
        <div class="hero-icon">
          <i class="mdi mdi-transit-connection-variant"></i>
        </div>
        <div class="hero-text">
          <h1>Shipments Management</h1>
          <p>Track logistics performance, commissions, and payment status in real time.</p>
        </div>
      </div>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="openDialog()">
          <i class="mdi mdi-plus"></i>
          Create Shipment
        </el-button>
        <el-button size="large" text @click="fetchShipments">
          <i class="mdi mdi-refresh"></i>
          Refresh
        </el-button>
      </div>
    </div>

    <el-card class="filters-card" shadow="never">
      <div class="filters-header">
        <div class="filters-title">
          <i class="mdi mdi-filter-variant"></i>
          <span>Quick filters</span>
        </div>
        <el-button text size="small" @click="resetFilters">Reset</el-button>
      </div>
      <div class="filters-grid">
        <el-input
          v-model="searchQuery"
          placeholder="Search by cargo, carrier, or vehicle"
          clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>
        <el-select v-model="paymentFilter" placeholder="Payment status" clearable>
          <el-option label="All status" value="" />
          <el-option label="Paid" value="paid" />
          <el-option label="Pending" value="pending" />
          <el-option label="Failed" value="failed" />
        </el-select>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="to"
          start-placeholder="Start date"
          end-placeholder="End date"
          value-format="YYYY-MM-DD"
          clearable
        />
        <div class="filters-stat">
          <span>Total revenue</span>
          <strong>{{ stats.totalRevenue.toFixed(2) }} TMT</strong>
        </div>
      </div>
    </el-card>

    <div class="stats-section">
      <el-card class="stat-card" shadow="hover">
        <div class="stat-icon total">
          <i class="mdi mdi-chart-timeline-variant"></i>
        </div>
        <div class="stat-body">
          <span class="label">Total Shipments</span>
          <span class="value">{{ shipments.length }}</span>
        </div>
      </el-card>
      <el-card class="stat-card" shadow="hover">
        <div class="stat-icon paid">
          <i class="mdi mdi-check-circle"></i>
        </div>
        <div class="stat-body">
          <span class="label">Paid</span>
          <span class="value">{{ stats.paid }}</span>
        </div>
      </el-card>
      <el-card class="stat-card" shadow="hover">
        <div class="stat-icon pending">
          <i class="mdi mdi-timer-sand"></i>
        </div>
        <div class="stat-body">
          <span class="label">Pending</span>
          <span class="value">{{ stats.pending }}</span>
        </div>
      </el-card>
      <el-card class="stat-card" shadow="hover">
        <div class="stat-icon revenue">
          <i class="mdi mdi-cash-multiple"></i>
        </div>
        <div class="stat-body">
          <span class="label">Commission Earned</span>
          <span class="value">{{ stats.totalRevenue.toFixed(2) }} TMT</span>
        </div>
      </el-card>
    </div>

    <el-card class="table-card" shadow="never">
      <div class="table-header">
        <div>
          <h3>Shipments overview</h3>
          <p>{{ filteredShipments.length }} results</p>
        </div>
        <el-button text @click="exportShipments">
          <i class="mdi mdi-download"></i>
          Export CSV
        </el-button>
      </div>
      <el-table
        :data="filteredShipments"
        style="width: 100%"
        class="modern-table"
        border={false}
      >
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
      <div v-if="!filteredShipments.length" class="empty-state">
        <div class="empty-icon">
          <i class="mdi mdi-truck-delivery"></i>
        </div>
        <h4>No shipments found</h4>
        <p>Try adjusting filters or create your first shipment.</p>
        <el-button type="primary" @click="openDialog()">
          <i class="mdi mdi-plus"></i>
          Create shipment
        </el-button>
      </div>
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
const dateRange = ref<[string, string] | null>(null)

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

  if (dateRange.value && dateRange.value.length === 2) {
    const [start, end] = dateRange.value
    const startDate = new Date(`${start}T00:00:00`)
    const endDate = new Date(`${end}T23:59:59`)

    filtered = filtered.filter(shipment => {
      const reference = shipment.start_time || shipment.end_time
      if (!reference) return false
      const current = new Date(reference)
      return current >= startDate && current <= endDate
    })
  }

  return filtered
})

function resetFilters() {
  searchQuery.value = ''
  paymentFilter.value = ''
  dateRange.value = null
}

function exportShipments() {
  const rows = filteredShipments.value
  if (!rows.length) {
    ElMessage.warning('No shipments to export')
    return
  }

  const header = ['Cargo', 'Carrier', 'Distance (km)', 'Total price (TMT)', 'Payment status', 'Commission (TMT)', 'Start time', 'End time']
  const body = rows.map(row => [
    row.cargo?.title || '',
    row.carrier?.username || '',
    row.distance_km ?? '',
    row.total_price ?? '',
    formatPaymentStatus(row.payment_status || ''),
    row.commission_amount ?? '',
    row.start_time ? formatTime(row.start_time) : '',
    row.end_time ? formatTime(row.end_time) : ''
  ])

  const csv = [header, ...body]
    .map(line => line.map(value => `"${String(value).replaceAll('"', '""')}"`).join(','))
    .join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `shipments-${Date.now()}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  ElMessage.success('Shipments exported')
}

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
.shipments-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 24px;
}

.page-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 24px;
  border-radius: 16px;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #fff;
  box-shadow: 0 20px 50px -20px rgba(15, 23, 42, 0.8);
}

.hero-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.hero-icon {
  width: 64px;
  height: 64px;
  border-radius: 18px;
  display: grid;
  place-items: center;
  background: rgba(255, 255, 255, 0.1);
  font-size: 30px;
}

.hero-text h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 6px;
}

.hero-text p {
  margin: 0;
  color: rgba(255, 255, 255, 0.75);
}

.hero-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.filters-card {
  border-radius: 16px;
  border: 1px solid rgba(15, 23, 42, 0.05);
  padding: 20px 24px;
}

.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1f2937;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(180px, 1fr));
  gap: 16px;
}

.filters-stat {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 12px 16px;
  border-radius: 12px;
  background: #f1f5f9;
  color: #0f172a;
  font-size: 14px;
}

.filters-stat strong {
  font-size: 18px;
  margin-top: 4px;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.stat-card {
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 20px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  border: none;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 45px -20px rgba(15, 23, 42, 0.35);
}

.stat-icon {
  width: 54px;
  height: 54px;
  border-radius: 14px;
  display: grid;
  place-items: center;
  font-size: 26px;
  color: #fff;
}

.stat-icon.total { background: linear-gradient(135deg, #6366f1, #4338ca); }
.stat-icon.paid { background: linear-gradient(135deg, #22c55e, #16a34a); }
.stat-icon.pending { background: linear-gradient(135deg, #f97316, #ea580c); }
.stat-icon.revenue { background: linear-gradient(135deg, #14b8a6, #0d9488); }

.stat-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-body .label {
  font-size: 13px;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.stat-body .value {
  font-size: 22px;
  font-weight: 700;
  color: #0f172a;
}

.table-card {
  border-radius: 16px;
  border: 1px solid rgba(15, 23, 42, 0.05);
  padding: 0;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(15, 23, 42, 0.05);
}

.table-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.table-header p {
  margin: 2px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.modern-table :deep(.el-table__header-wrapper) {
  background: #f8fafc;
}

.modern-table :deep(th) {
  background: transparent;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 12px;
  color: #64748b;
}

.modern-table :deep(.el-table__row) {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.modern-table :deep(.el-table__row:hover) {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -12px rgba(15, 23, 42, 0.2);
}

.cargo-cell,
.carrier-cell,
.details-cell,
.commission-cell,
.timeline-cell,
.action-buttons {
  display: flex;
  align-items: center;
  gap: 8px;
}

.details-cell {
  flex-wrap: wrap;
  gap: 12px;
}

.detail-item,
.time-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #475569;
}

.payment-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-transform: capitalize;
  font-weight: 600;
  border-radius: 20px;
  padding: 2px 10px;
}

.payment-paid { background: rgba(34, 197, 94, 0.12); color: #16a34a; }
.payment-pending { background: rgba(249, 115, 22, 0.12); color: #ea580c; }
.payment-failed { background: rgba(239, 68, 68, 0.12); color: #dc2626; }

.action-buttons {
  gap: 6px;
}

.action-buttons .el-button {
  font-size: 18px;
}

.empty-state {
  display: grid;
  place-items: center;
  padding: 32px 24px 40px;
  text-align: center;
  color: #475569;
  gap: 12px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: #f1f5f9;
  color: #0f172a;
  font-size: 32px;
}

.shipment-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.form-item-full {
  grid-column: span 2;
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 12px;
}

@media (max-width: 1200px) {
  .filters-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stats-section {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 992px) {
  .page-hero {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-actions {
    width: 100%;
    justify-content: flex-start;
  }

  .filters-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .shipments-page {
    padding: 16px;
  }

  .hero-info {
    flex-direction: column;
    align-items: flex-start;
  }

  .hero-icon {
    width: 56px;
    height: 56px;
  }

  .hero-text h1 {
    font-size: 24px;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }

  .filters-card {
    padding: 16px;
  }

  .stats-section {
    grid-template-columns: 1fr;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-item-full {
    grid-column: span 1;
  }

  .table-card {
    overflow: hidden;
  }

  .modern-table :deep(.el-table__body-wrapper) {
    overflow-x: auto;
  }
}

@media (max-width: 480px) {
  .page-hero {
    padding: 18px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .filters-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .dialog-footer {
    flex-direction: column;
  }

  .dialog-footer .el-button {
    width: 100%;
  }
}

@media (max-width: 360px) {
  .hero-text h1 {
    font-size: 20px;
  }

  .filters-card {
    padding: 12px;
  }
}

</style>
