<template>
  <div class="offers-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-handshake-outline"></i>
            {{ $t('offers.title') }}
          </h1>
          <p class="page-subtitle">{{ $t('offers.subtitle') }}</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" size="large" @click="openDialog()" class="add-btn">
            <i class="mdi mdi-plus"></i>
            {{ $t('offers.createOffer') }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            :placeholder="$t('offers.searchPlaceholder')"
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="statusFilter" :placeholder="$t('offers.filterByStatus')" clearable class="status-filter">
          <el-option :label="$t('offers.allStatus')" value="" />
          <el-option :label="$t('offers.pending')" value="pending" />
          <el-option :label="$t('offers.accepted')" value="accepted" />
          <el-option :label="$t('offers.rejected')" value="rejected" />
        </el-select>

        <el-button class="filter-btn" @click="fetchOffers">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-handshake"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ offers.length }}</div>
          <div class="stat-label">{{ $t('offers.totalOffers') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pending">
          <i class="mdi mdi-clock-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pending }}</div>
          <div class="stat-label">{{ $t('offers.pending') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon accepted">
          <i class="mdi mdi-check-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.accepted }}</div>
          <div class="stat-label">{{ $t('offers.accepted') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon average">
          <i class="mdi mdi-cash"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.averagePrice.toFixed(0) }}</div>
          <div class="stat-label">{{ $t('offers.averagePrice') }}</div>
        </div>
      </div>
    </div>

    <!-- Offers Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredOffers" style="width: 100%" class="modern-table">
        <el-table-column :label="$t('offers.cargo')" min-width="220">
          <template #default="{ row }">
            <div class="cargo-cell">
              <i class="mdi mdi-package-variant-closed"></i>
              <span>{{ row.cargo?.title || $t('common.noData') }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column :label="$t('offers.carrier')" min-width="180">
          <template #default="{ row }">
            <div class="carrier-cell">
              <el-avatar :size="32" class="carrier-avatar">
                <i class="mdi mdi-account"></i>
              </el-avatar>
              <span>{{ row.carrier?.username || $t('common.noData') }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column :label="$t('offers.price')" width="140">
          <template #default="{ row }">
            <div class="price-cell">
              <i class="mdi mdi-cash"></i>
              <span>{{ row.price }} TMT</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column :label="$t('offers.vehicle')" min-width="180">
          <template #default="{ row }">
            <div class="vehicle-cell" v-if="row.vehicle">
              <i class="mdi mdi-truck"></i>
              <span>{{ getVehicleLabel(row.vehicle) }}</span>
            </div>
            <span v-else class="no-vehicle">{{ $t('offers.noVehicle') }}</span>
          </template>
        </el-table-column>

        <el-table-column :label="$t('offers.note')" min-width="200">
          <template #default="{ row }">
            <div class="note-cell">
              <i class="mdi mdi-note-text-outline"></i>
              <span>{{ row.note || $t('offers.noNotes') }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column :label="$t('offers.status')" width="140">
          <template #default="{ row }">
            <el-tag
                :type="statusType(row.status)"
                :class="`status-tag status-${row.status}`"
                effect="plain"
            >
              <i :class="statusIcon(row.status)"></i>
              {{ formatStatus(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column fixed="right" :label="$t('common.actions')" width="160">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-tooltip :content="$t('common.edit')" placement="top">
                <el-button link type="primary" @click="openDialog(row)">
                  <i class="mdi mdi-pencil"></i>
                </el-button>
              </el-tooltip>
              <el-tooltip :content="$t('common.viewDetails')" placement="top">
                <el-button link type="info">
                  <i class="mdi mdi-eye"></i>
                </el-button>
              </el-tooltip>
              <el-popconfirm
                  :title="$t('offers.deleteConfirm')"
                  @confirm="deleteOffer(row.id!)"
              >
                <template #reference>
                  <el-tooltip :content="$t('common.delete')" placement="top">
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
        :title="form.id ? $t('offers.editOffer') : $t('offers.createNew')"
        width="600px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="offer-form">
        <el-form-item :label="$t('offers.cargo')">
          <el-select v-model="form.cargo" :placeholder="$t('offers.selectCargo')" filterable style="width:100%">
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

        <el-form-item :label="$t('offers.price')">
          <el-input-number v-model="form.price" :min="0" :step="10" style="width:100%" />
        </el-form-item>

        <el-form-item :label="`${t('offers.vehicle')} (${t('offers.optional')})`">
          <el-select v-model="form.vehicle" :placeholder="$t('offers.selectVehicle')" filterable clearable style="width:100%">
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

        <el-form-item :label="$t('offers.note')">
          <el-input
              v-model="form.note"
              type="textarea"
              :rows="3"
              :placeholder="$t('offers.addNotes')"
              maxlength="300"
              show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button size="large" @click="dialogVisible = false">
            <i class="mdi mdi-close"></i>
            {{ $t('common.cancel') }}
          </el-button>
          <el-button type="primary" size="large" @click="saveOffer">
            <i class="mdi mdi-check"></i>
            {{ form.id ? $t('offers.editOffer') : $t('offers.createOffer') }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useI18n } from 'vue-i18n'
import {
  getOffers as apiGetOffers,
  createOffer as apiCreateOffer,
  updateOffer as apiUpdateOffer,
  deleteOffer as apiDeleteOffer,
  getCargos as apiGetCargos,
  getVehicles as apiGetVehicles
} from '@/api/api'

interface Offer {
  id?: number
  cargo: any
  carrier?: { id: number; username: string }
  price: number
  note?: string
  status?: string
  vehicle?: any
}

interface CargoOption {
  id: number
  title: string
}

interface VehicleOption {
  id: number
  plate_number: string
  brand: string
  model: string
  capacity_kg: number
}

const { t } = useI18n()

const offers = ref<Offer[]>([])
const cargoOptions = ref<CargoOption[]>([])
const vehicleOptions = ref<VehicleOption[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')

const form = ref<Offer>({ cargo: null, price: 0, note: '', vehicle: null })

// Computed stats
const stats = computed(() => {
  const pending = offers.value.filter(o => o.status === 'pending').length
  const accepted = offers.value.filter(o => o.status === 'accepted').length
  const total = offers.value.length
  const sum = offers.value.reduce((acc, o) => acc + o.price, 0)

  return {
    pending,
    accepted,
    averagePrice: total > 0 ? sum / total : 0,
  }
})

// Filtered offers
const filteredOffers = computed(() => {
  let filtered = offers.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(offer =>
      offer.cargo?.title?.toLowerCase().includes(query) ||
      offer.carrier?.username?.toLowerCase().includes(query) ||
      offer.note?.toLowerCase().includes(query)
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(offer => offer.status === statusFilter.value)
  }

  return filtered
})

function statusType(status?: string) {
  if (status === 'accepted') return 'success'
  if (status === 'rejected') return 'danger'
  return 'warning'
}

function statusIcon(status?: string) {
  switch (status) {
    case 'accepted': return 'mdi mdi-check-circle'
    case 'rejected': return 'mdi mdi-close-circle'
    case 'pending': return 'mdi mdi-clock-outline'
    default: return 'mdi mdi-help-circle'
  }
}

function formatStatus(status?: string) {
  switch (status) {
    case 'accepted': return t('offers.accepted')
    case 'rejected': return t('offers.rejected')
    case 'pending':
    default: return t('offers.pending')
  }
}

function getVehicleLabel(vehicle: any) {
  if (typeof vehicle === 'number') {
    const v = vehicleOptions.value.find(vo => vo.id === vehicle)
    return v ? `${v.plate_number} (${v.capacity_kg}kg)` : 'Unknown'
  }
  return vehicle?.plate_number ? `${vehicle.plate_number} (${vehicle.capacity_kg}kg)` : 'Unknown'
}

async function fetchOffers() {
  const { data } = await apiGetOffers()
  offers.value = data
}

async function fetchOptions() {
  const { data: cargos } = await apiGetCargos()
  cargoOptions.value = cargos
  const { data: vehicles } = await apiGetVehicles()
  vehicleOptions.value = vehicles
}

function openDialog(offer?: Offer) {
  if (offer) {
    form.value = {
      ...offer,
      cargo: offer.cargo?.id || offer.cargo,
      vehicle: offer.vehicle?.id || offer.vehicle
    }
  } else {
    form.value = { cargo: null, price: 0, note: '', vehicle: null }
  }
  dialogVisible.value = true
}

async function saveOffer() {
  if (form.value.id) {
    await apiUpdateOffer(form.value.id, form.value)
    ElMessage.success(t('offers.offerUpdated'))
  } else {
    await apiCreateOffer(form.value)
    ElMessage.success(t('offers.offerCreated'))
  }
  dialogVisible.value = false
  await fetchOffers()
}

async function deleteOffer(id: number) {
  await apiDeleteOffer(id)
  ElMessage.success(t('offers.offerDeleted'))
  await fetchOffers()
}

onMounted(async () => {
  await fetchOptions()
  await fetchOffers()
})
</script>

<style scoped>
.offers-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.header-left {
  flex: 1;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #3b82f6;
  font-size: 32px;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
  margin: 0;
}

.add-btn {
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.add-btn i {
  margin-right: 6px;
  font-size: 18px;
}

/* Filters Card */
.filters-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.filters-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.status-filter {
  width: 180px;
}

.filter-btn {
  padding: 12px;
  font-size: 20px;
  border-radius: 8px;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
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

.stat-icon.total {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.pending {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.accepted {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.average {
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

/* Table Card */
.table-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.modern-table {
  border-radius: 8px;
  overflow: hidden;
}

.modern-table :deep(.el-table__header) {
  background: #f8fafc;
}

.modern-table :deep(th) {
  background: #f8fafc !important;
  color: #475569;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-table :deep(.el-table__row:hover) {
  background: #f8fafc;
}

.cargo-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #0f172a;
}

.cargo-cell i {
  color: #3b82f6;
  font-size: 18px;
}

.carrier-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #475569;
}

.carrier-avatar {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.price-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  color: #10b981;
  font-size: 15px;
}

.price-cell i {
  font-size: 18px;
}

.vehicle-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
}

.vehicle-cell i {
  color: #94a3b8;
  font-size: 16px;
}

.no-vehicle {
  color: #cbd5e1;
  font-style: italic;
  font-size: 13px;
}

.note-cell {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
  line-height: 1.5;
}

.note-cell i {
  color: #94a3b8;
  font-size: 16px;
  margin-top: 2px;
  flex-shrink: 0;
}

.status-tag {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.status-tag i {
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  align-items: center;
}

.action-buttons :deep(.el-button) {
  font-size: 18px;
  padding: 8px;
  transition: all 0.3s ease;
}

.action-buttons :deep(.el-button:hover) {
  transform: scale(1.1);
}

/* Dialog Styles */
.modern-dialog :deep(.el-dialog) {
  border-radius: 16px;
  overflow: hidden;
}

.modern-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  padding: 20px 24px;
  margin: 0;
}

.modern-dialog :deep(.el-dialog__title) {
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.modern-dialog :deep(.el-dialog__headerbtn .el-dialog__close) {
  color: white;
  font-size: 20px;
}

.modern-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.offer-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.offer-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.offer-form :deep(.el-textarea__inner) {
  border-radius: 8px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.option-item i {
  color: #3b82f6;
  font-size: 16px;
}

.dialog-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.dialog-footer .el-button {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
}

.dialog-footer .el-button i {
  margin-right: 6px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .filters-container {
    flex-direction: column;
  }

  .search-input,
  .status-filter {
    width: 100%;
    max-width: none;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
