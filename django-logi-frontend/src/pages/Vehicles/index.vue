<template>
  <div class="vehicles-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-truck"></i>
            {{ $t('vehicles.title') }}
          </h1>
          <p class="page-subtitle">{{ $t('vehicles.subtitle') }}</p>
        </div>
        <div class="header-actions">
          <router-link to="/vehicles/add">
            <el-button type="primary" size="large" class="add-btn">
              <i class="mdi mdi-plus"></i>
              {{ $t('vehicles.addNew') }}
            </el-button>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Route Prefilter Summary (from marketplace) -->
    <el-alert
      v-if="prefilterSummary"
      :title="prefilterSummary"
      type="info"
      class="prefilter-banner"
      show-icon
      :closable="false"
    />

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            :placeholder="$t('vehicles.searchPlaceholder') as string"
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="typeFilter" :placeholder="$t('vehicles.filterByType') as string" clearable class="type-filter">
          <el-option :label="$t('vehicles.allTypes') as string" value="" />
          <el-option :label="$t('vehicles.boxTruck') as string" value="box" />
          <el-option :label="$t('vehicles.flatbed') as string" value="flatbed" />
          <el-option :label="$t('vehicles.refrigerated') as string" value="refrigerated" />
          <el-option :label="$t('vehicles.tanker') as string" value="tanker" />
        </el-select>

        <el-select v-model="gpsFilter" :placeholder="$t('vehicles.gpsStatus') as string" clearable class="gps-filter">
          <el-option :label="$t('vehicles.allVehicles') as string" value="" />
          <el-option :label="$t('vehicles.gpsEnabled') as string" value="enabled" />
          <el-option :label="$t('vehicles.disabled') as string" value="disabled" />
        </el-select>

        <el-button class="filter-btn" @click="fetchVehicles">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-truck-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ vehicles.length }}</div>
          <div class="stat-label">{{ $t('vehicles.totalVehicles') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon gps">
          <i class="mdi mdi-map-marker-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.gpsEnabled }}</div>
          <div class="stat-label">{{ $t('vehicles.gpsEnabledCount') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon capacity">
          <i class="mdi mdi-weight-kilogram"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalCapacity.toFixed(0) }}</div>
          <div class="stat-label">{{ $t('vehicles.totalCapacity') }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon volume">
          <i class="mdi mdi-cube-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalVolume.toFixed(1) }}</div>
          <div class="stat-label">{{ $t('vehicles.totalVolume') }}</div>
        </div>
      </div>
    </div>

    <!-- Vehicles Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredVehicles" style="width: 100%" class="modern-table">
        <el-table-column prop="plate_number" label="Plate Number" width="140">
          <template #default="scope">
            <div class="plate-number">
              <i class="mdi mdi-card-text"></i>
              <span>{{ scope.row.plate_number }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Vehicle Info" min-width="220">
          <template #default="scope">
            <div class="vehicle-info">
              <div class="vehicle-name">{{ scope.row.brand }} {{ scope.row.model }}</div>
              <div class="vehicle-meta">
                <span class="year">
                  <i class="mdi mdi-calendar"></i>
                  {{ scope.row.year }}
                </span>
                <span class="type">
                  <i class="mdi mdi-truck-cargo-container"></i>
                  {{ scope.row.truck_type }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Specifications" min-width="200">
          <template #default="scope">
            <div class="specs">
              <div class="spec-item">
                <i class="mdi mdi-weight-kilogram"></i>
                <span>{{ scope.row.capacity_kg }} kg</span>
              </div>
              <div class="spec-item">
                <i class="mdi mdi-cube-outline"></i>
                <span>{{ scope.row.volume_m3 }} m³</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="gps_enabled" label="GPS" width="120">
          <template #default="scope">
            <el-tag 
                :type="scope.row.gps_enabled ? 'success' : 'info'"
                :class="`gps-tag ${scope.row.gps_enabled ? 'enabled' : 'disabled'}`"
                effect="plain"
            >
              <i :class="scope.row.gps_enabled ? 'mdi mdi-map-marker-check' : 'mdi mdi-map-marker-off'"></i>
              {{ scope.row.gps_enabled ? 'Enabled' : 'Disabled' }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Photo" width="100">
          <template #default="scope">
            <el-image
                v-if="scope.row.photo"
                :src="scope.row.photo"
                :preview-src-list="[scope.row.photo]"
                class="vehicle-photo"
                fit="cover"
            >
              <template #error>
                <div class="image-placeholder">
                  <i class="mdi mdi-image-off"></i>
                </div>
              </template>
            </el-image>
            <div v-else class="image-placeholder">
              <i class="mdi mdi-truck"></i>
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
                  title="Are you sure to delete this vehicle?"
                  @confirm="deleteVehicle(scope.row.id)"
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
        :title="form.id ? 'Edit Vehicle' : 'Add New Vehicle'" 
        width="700px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="vehicle-form">
        <div class="form-grid">
          <el-form-item label="Plate Number" class="form-item-full">
            <el-input v-model="form.plate_number" placeholder="Enter plate number">
              <template #prefix>
                <i class="mdi mdi-card-text"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Brand">
            <el-input v-model="form.brand" placeholder="e.g., Mercedes">
              <template #prefix>
                <i class="mdi mdi-factory"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Model">
            <el-input v-model="form.model" placeholder="e.g., Actros">
              <template #prefix>
                <i class="mdi mdi-truck"></i>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="Year">
            <el-input-number v-model="form.year" :min="1900" :max="2100" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Truck Type">
            <el-select v-model="form.truck_type" placeholder="Select type" style="width: 100%">
              <el-option label="Box Truck" value="box" />
              <el-option label="Flatbed" value="flatbed" />
              <el-option label="Refrigerated" value="refrigerated" />
              <el-option label="Tanker" value="tanker" />
              <el-option label="Other" value="other" />
            </el-select>
          </el-form-item>

          <el-form-item label="Capacity (kg)">
            <el-input-number v-model="form.capacity_kg" :min="0" :step="100" style="width: 100%" />
          </el-form-item>

          <el-form-item label="Volume (m³)">
            <el-input-number v-model="form.volume_m3" :min="0" :step="0.5" style="width: 100%" />
          </el-form-item>

          <el-form-item label="GPS Tracking" class="gps-switch-item">
            <div class="switch-wrapper">
              <el-switch v-model="form.gps_enabled" size="large" />
              <span class="switch-label">{{ form.gps_enabled ? 'Enabled' : 'Disabled' }}</span>
            </div>
          </el-form-item>

          <el-form-item label="Vehicle Photo" class="form-item-full">
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
          <el-button type="primary" size="large" @click="saveVehicle">
            <i class="mdi mdi-check"></i>
            {{ form.id ? 'Update' : 'Create' }} Vehicle
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getVehicles, createVehicle, updateVehicle, deleteVehicleApi } from '@/api/api'

interface Vehicle {
  id?: number
  plate_number: string
  brand: string
  model: string
  year: number | null
  capacity_kg: number
  volume_m3: number
  truck_type: string
  gps_enabled: boolean
  photo?: string
}

const vehicles = ref<Vehicle[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const typeFilter = ref('')
const gpsFilter = ref('')

// Prefilter summary from marketplace route query
const route = useRoute()
const prefilterSummary = computed(() => {
  const from = (route.query.from as string) || ''
  const to = (route.query.to as string) || ''
  const date = (route.query.date as string) || ''
  const radius = route.query.radius as string | undefined
  if (!from && !to && !date && !radius) return ''
  const parts: string[] = []
  if (from) parts.push(`From: ${from}`)
  if (to) parts.push(`To: ${to}`)
  if (date) parts.push(`Date: ${date}`)
  if (radius) parts.push(`Radius: ${radius} km`)
  return `Searching vehicles — ${parts.join(' • ')}`
})

const form = ref<Vehicle>({
  plate_number: '',
  brand: '',
  model: '',
  year: null,
  capacity_kg: 0,
  volume_m3: 0,
  truck_type: '',
  gps_enabled: false
})
let file: File | null = null

// Computed stats
const stats = computed(() => {
  return {
    gpsEnabled: vehicles.value.filter(v => v.gps_enabled).length,
    totalCapacity: vehicles.value.reduce((sum, v) => sum + v.capacity_kg, 0),
    totalVolume: vehicles.value.reduce((sum, v) => sum + v.volume_m3, 0),
  }
})

// Filtered vehicles
const filteredVehicles = computed(() => {
  let filtered = vehicles.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(vehicle =>
        vehicle.plate_number.toLowerCase().includes(query) ||
        vehicle.brand.toLowerCase().includes(query) ||
        vehicle.model.toLowerCase().includes(query) ||
        vehicle.truck_type.toLowerCase().includes(query)
    )
  }

  // Filter by type
  if (typeFilter.value) {
    filtered = filtered.filter(vehicle => vehicle.truck_type === typeFilter.value)
  }

  // Filter by GPS status
  if (gpsFilter.value) {
    const isEnabled = gpsFilter.value === 'enabled'
    filtered = filtered.filter(vehicle => vehicle.gps_enabled === isEnabled)
  }

  return filtered
})

async function fetchVehicles() {
  const { data } = await getVehicles()
  vehicles.value = data
}

function openDialog(vehicle?: Vehicle) {
  if (vehicle) {
    form.value = { ...vehicle }
  } else {
    form.value = { 
      plate_number: '',
      brand: '',
      model: '',
      year: null,
      capacity_kg: 0,
      volume_m3: 0,
      truck_type: '',
      gps_enabled: false 
    }
  }
  file = null
  dialogVisible.value = true
}

function onFileChange(uploadFile: any) {
  file = uploadFile.raw
}

async function saveVehicle() {
  const formData = new FormData()
  Object.entries(form.value).forEach(([key, val]) => {
    if (val !== null && val !== undefined) formData.append(key, String(val))
  })
  if (file) formData.append('photo', file)

  if (form.value.id) {
    await updateVehicle(form.value.id, formData)
    ElMessage.success('Vehicle updated successfully')
  } else {
    await createVehicle(formData)
    ElMessage.success('Vehicle created successfully')
  }
  dialogVisible.value = false
  await fetchVehicles()
}

async function deleteVehicle(id: number) {
  await deleteVehicleApi(id)
  ElMessage.success('Vehicle deleted successfully')
  await fetchVehicles()
}

onMounted(fetchVehicles)
</script>

<style scoped>
.vehicles-page {
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

.type-filter,
.gps-filter {
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

.stat-icon.gps {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.capacity {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.stat-icon.volume {
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

.plate-number {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  color: #0f172a;
  font-family: monospace;
  font-size: 15px;
}

.plate-number i {
  color: #3b82f6;
  font-size: 18px;
}

.vehicle-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.vehicle-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 15px;
}

.vehicle-meta {
  display: flex;
  gap: 12px;
  font-size: 13px;
  color: #64748b;
}

.vehicle-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.vehicle-meta i {
  color: #94a3b8;
  font-size: 14px;
}

.specs {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.spec-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
}

.spec-item i {
  color: #94a3b8;
  font-size: 16px;
}

.gps-tag {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.gps-tag i {
  font-size: 14px;
}

.vehicle-photo {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.vehicle-photo:hover {
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

.vehicle-form {
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

.vehicle-form :deep(.el-form-item__label) {
  font-weight: 600;
  color: #334155;
  margin-bottom: 8px;
}

.vehicle-form :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.gps-switch-item {
  display: flex;
  align-items: center;
}

.switch-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.switch-label {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
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
  .type-filter,
  .gps-filter {
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
