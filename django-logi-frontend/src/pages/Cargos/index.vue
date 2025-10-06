<template>
  <div class="cargos-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-package-variant-closed"></i>
            Cargos Management
          </h1>
          <p class="page-subtitle">Manage and track all your cargo shipments</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" size="large" @click="openDialog()" class="add-btn">
            <i class="mdi mdi-plus"></i>
            Add New Cargo
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            placeholder="Search cargos by title, address..."
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="statusFilter" placeholder="Filter by Status" clearable class="status-filter">
          <el-option label="All Status" value="" />
          <el-option label="Open" value="open" />
          <el-option label="In Progress" value="in_progress" />
          <el-option label="Delivered" value="delivered" />
          <el-option label="Cancelled" value="cancelled" />
        </el-select>

        <el-button class="filter-btn" @click="fetchCargos">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon open">
          <i class="mdi mdi-package-variant"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.open }}</div>
          <div class="stat-label">Open</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon progress">
          <i class="mdi mdi-truck-fast"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.in_progress }}</div>
          <div class="stat-label">In Progress</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon delivered">
          <i class="mdi mdi-check-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.delivered }}</div>
          <div class="stat-label">Delivered</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-package-variant-closed"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ cargos.length }}</div>
          <div class="stat-label">Total Cargos</div>
        </div>
      </div>
    </div>

    <!-- Cargos Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredCargos" style="width: 100%" class="modern-table">
        <el-table-column prop="title" label="Title" min-width="180">
          <template #default="scope">
            <div class="cargo-title">
              <i class="mdi mdi-package-variant-closed"></i>
              <span>{{ scope.row.title }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="Details" min-width="200">
          <template #default="scope">
            <div class="cargo-details">
              <div class="detail-item">
                <i class="mdi mdi-weight-kilogram"></i>
                <span>{{ scope.row.weight_kg }} kg</span>
              </div>
              <div class="detail-item">
                <i class="mdi mdi-cube-outline"></i>
                <span>{{ scope.row.volume_m3 }} m³</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Route" min-width="250">
          <template #default="scope">
            <div class="route-info">
              <div class="route-item">
                <i class="mdi mdi-map-marker-up"></i>
                <span>{{ scope.row.pickup_address }}</span>
              </div>
              <div class="route-arrow">
                <i class="mdi mdi-arrow-down"></i>
              </div>
              <div class="route-item">
                <i class="mdi mdi-map-marker-down"></i>
                <span>{{ scope.row.delivery_address }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="pickup_date" label="Pickup Date" width="140" />
        
        <el-table-column prop="status" label="Status" width="140">
          <template #default="scope">
            <el-tag
                :type="statusTag(scope.row.status)"
                :class="`status-tag status-${scope.row.status}`"
                effect="plain"
            >
              {{ formatStatus(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Photo" width="100">
          <template #default="scope">
            <el-image
                v-if="scope.row.photo"
                :src="scope.row.photo"
                :preview-src-list="[scope.row.photo]"
                class="cargo-photo"
                fit="cover"
            >
              <template #error>
                <div class="image-placeholder">
                  <i class="mdi mdi-image-off"></i>
                </div>
              </template>
            </el-image>
            <div v-else class="image-placeholder">
              <i class="mdi mdi-image-off"></i>
            </div>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Actions" width="160">
          <template #default="scope">
            <div class="action-buttons">
              <el-tooltip content="Edit" placement="top">
                <el-button link type="primary" @click="openDialog(scope.row)">
                  <i class="mdi mdi-pencil"></i>
                </el-button>
              </el-tooltip>
              <el-tooltip content="View Details" placement="top">
                <el-button link type="info">
                  <i class="mdi mdi-eye"></i>
                </el-button>
              </el-tooltip>
              <el-popconfirm
                  title="Are you sure to delete this cargo?"
                  @confirm="deleteCargo(scope.row.id)"
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
        :title="form.id ? 'Edit Cargo' : 'Create New Cargo'" 
        width="700px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="cargo-form">
        <div class="form-grid">
          <el-form-item label="Title" class="form-item-full">
            <el-input v-model="form.title" placeholder="Enter cargo title">
              <template #prefix>
                <i class="mdi mdi-text"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Description" class="form-item-full">
            <el-input 
                v-model="form.description" 
                type="textarea" 
                :rows="3" 
                placeholder="Enter cargo description"
            />
          </el-form-item>

          <el-form-item label="Weight (kg)">
            <el-input-number v-model="form.weight_kg" :min="0" :step="0.1" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Volume (m³)">
            <el-input-number v-model="form.volume_m3" :min="0" :step="0.1" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Pickup Address" class="form-item-full">
            <el-input v-model="form.pickup_address" placeholder="Enter pickup address">
              <template #prefix>
                <i class="mdi mdi-map-marker-up"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Delivery Address" class="form-item-full">
            <el-input v-model="form.delivery_address" placeholder="Enter delivery address">
              <template #prefix>
                <i class="mdi mdi-map-marker-down"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Pickup Date">
            <el-date-picker
                v-model="form.pickup_date"
                type="date"
                placeholder="Select pickup date"
                style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="Delivery Date">
            <el-date-picker
                v-model="form.delivery_date"
                type="date"
                placeholder="Select delivery date (optional)"
                style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="Price Offer">
            <el-input-number v-model="form.price_offer" :min="0" :step="10" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Status">
            <el-select v-model="form.status" style="width: 100%">
              <el-option label="Open" value="open" />
              <el-option label="In Progress" value="in_progress" />
              <el-option label="Delivered" value="delivered" />
              <el-option label="Cancelled" value="cancelled" />
            </el-select>
          </el-form-item>

          <el-form-item label="Photo" class="form-item-full">
            <el-upload
                class="photo-uploader"
                :auto-upload="false"
                :show-file-list="false"
                :on-change="onFileChange"
                drag
            >
              <div class="upload-content">
                <i class="mdi mdi-cloud-upload"></i>
                <div class="upload-text">
                  <p>Drop file here or <em>click to upload</em></p>
                  <p class="upload-hint">Support: JPG, PNG (max 5MB)</p>
                </div>
              </div>
            </el-upload>
          </el-form-item>
        </div>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button size="large" @click="dialogVisible = false">
            <i class="mdi mdi-close"></i>
            Cancel
          </el-button>
          <el-button type="primary" size="large" @click="saveCargo">
            <i class="mdi mdi-check"></i>
            {{ form.id ? 'Update' : 'Create' }} Cargo
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
  getCargos as apiGetCargos,
  createCargo as apiCreateCargo,
  updateCargo as apiUpdateCargo,
  deleteCargo as apiDeleteCargo
} from '@/api/api'

interface Cargo {
  id?: number
  title: string
  description: string
  weight_kg: number
  volume_m3: number
  pickup_address: string
  delivery_address: string
  pickup_date: string | null
  delivery_date: string | null
  price_offer: number | null
  status: string
  photo?: string
}

const cargos = ref<Cargo[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')

const form = ref<Cargo>({
  title: '',
  description: '',
  weight_kg: 0,
  volume_m3: 0,
  pickup_address: '',
  delivery_address: '',
  pickup_date: null,
  delivery_date: null,
  price_offer: null,
  status: 'open'
})
let file: File | null = null

// Computed stats
const stats = computed(() => {
  return {
    open: cargos.value.filter(c => c.status === 'open').length,
    in_progress: cargos.value.filter(c => c.status === 'in_progress').length,
    delivered: cargos.value.filter(c => c.status === 'delivered').length,
  }
})

// Filtered cargos based on search and status
const filteredCargos = computed(() => {
  let filtered = cargos.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(cargo =>
        cargo.title.toLowerCase().includes(query) ||
        cargo.pickup_address.toLowerCase().includes(query) ||
        cargo.delivery_address.toLowerCase().includes(query)
    )
  }

  // Filter by status
  if (statusFilter.value) {
    filtered = filtered.filter(cargo => cargo.status === statusFilter.value)
  }

  return filtered
})

function statusTag(status: string) {
  switch (status) {
    case 'open':
      return 'info'
    case 'in_progress':
      return 'warning'
    case 'delivered':
      return 'success'
    case 'cancelled':
      return 'danger'
    default:
      return ''
  }
}

function formatStatus(status: string) {
  return status.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1)
  ).join(' ')
}

async function fetchCargos() {
  const { data } = await apiGetCargos()
  cargos.value = data
}

function openDialog(cargo?: Cargo) {
  if (cargo) {
    form.value = { ...cargo }
  } else {
    form.value = {
      title: '',
      description: '',
      weight_kg: 0,
      volume_m3: 0,
      pickup_address: '',
      delivery_address: '',
      pickup_date: null,
      delivery_date: null,
      price_offer: null,
      status: 'open'
    }
  }
  file = null
  dialogVisible.value = true
}

function onFileChange(uploadFile: any) {
  file = uploadFile.raw
}

async function saveCargo() {
  const formData = new FormData()
  Object.entries(form.value).forEach(([key, val]) => {
    if (val !== null && val !== undefined) formData.append(key, String(val))
  })
  if (file) formData.append('photo', file)

  if (form.value.id) {
    await apiUpdateCargo(form.value.id, formData)
    ElMessage.success('Cargo updated successfully')
  } else {
    await apiCreateCargo(formData)
    ElMessage.success('Cargo created successfully')
  }
  dialogVisible.value = false
  await fetchCargos()
}

async function deleteCargo(id: number) {
  await apiDeleteCargo(id)
  ElMessage.success('Cargo deleted successfully')
  await fetchCargos()
}

onMounted(fetchCargos)
</script>

<style scoped>
.cargos-page {
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
  width: 200px;
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

.stat-icon.open {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.stat-icon.progress {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.delivered {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.total {
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

.cargo-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: #0f172a;
}

.cargo-title i {
  color: #3b82f6;
  font-size: 18px;
}

.cargo-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
}

.detail-item i {
  color: #94a3b8;
  font-size: 16px;
}

.route-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.route-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}

.route-item i {
  color: #3b82f6;
  font-size: 16px;
}

.route-arrow {
  text-align: center;
  color: #cbd5e1;
  font-size: 12px;
  margin: 2px 0;
}

.status-tag {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
}

.cargo-photo {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cargo-photo:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.image-placeholder {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #cbd5e1;
  font-size: 24px;
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

.cargo-form {
  margin-top: 8px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-item-full {
  grid-column: 1 / -1;
}

.cargo-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.cargo-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.cargo-form :deep(.el-textarea__inner) {
  border-radius: 8px;
}

.photo-uploader :deep(.el-upload-dragger) {
  border-radius: 8px;
  border: 2px dashed #cbd5e1;
  background: #f8fafc;
  padding: 30px;
  transition: all 0.3s ease;
}

.photo-uploader :deep(.el-upload-dragger:hover) {
  border-color: #3b82f6;
  background: #eff6ff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-content i {
  font-size: 48px;
  color: #3b82f6;
}

.upload-text {
  text-align: center;
}

.upload-text p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.upload-text em {
  color: #3b82f6;
  font-style: normal;
  font-weight: 600;
}

.upload-hint {
  font-size: 12px !important;
  color: #94a3b8 !important;
  margin-top: 4px !important;
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

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
