<template>
  <div class="page">
    <PageHeader title="Vehicles">
      <template #actions>
        <el-button type="primary" @click="openDialog()" icon="Plus">Add Vehicle</el-button>
      </template>
    </PageHeader>

    <el-card shadow="hover" class="mt-4">
      <el-table :data="vehicles" stripe border style="width: 100%">
        <el-table-column prop="plate_number" label="Plate" width="120" />
        <el-table-column prop="brand" label="Brand" />
        <el-table-column prop="model" label="Model" />
        <el-table-column prop="year" label="Year" width="90" />
        <el-table-column prop="capacity_kg" label="Capacity (kg)" width="130" />
        <el-table-column prop="volume_m3" label="Volume (m³)" width="130" />
        <el-table-column prop="truck_type" label="Type" />
        <el-table-column prop="gps_enabled" label="GPS" width="90">
          <template #default="scope">
            <el-tag :type="scope.row.gps_enabled ? 'success' : 'info'">
              {{ scope.row.gps_enabled ? 'Yes' : 'No' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Photo" width="120">
          <template #default="scope">
            <el-image
                v-if="scope.row.photo"
                :src="scope.row.photo"
                style="width:80px; height:60px; object-fit:cover;"
            />
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="Actions" width="180">
          <template #default="scope">
            <el-button size="small" @click="openDialog(scope.row)">Edit</el-button>
            <el-popconfirm
                title="Delete this vehicle?"
                @confirm="deleteVehicle(scope.row.id)"
            >
              <template #reference>
                <el-button size="small" type="danger">Delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog for create/update -->
    <el-dialog v-model="dialogVisible" title="Vehicle" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="Plate Number">
          <el-input v-model="form.plate_number" />
        </el-form-item>
        <el-form-item label="Brand">
          <el-input v-model="form.brand" />
        </el-form-item>
        <el-form-item label="Model">
          <el-input v-model="form.model" />
        </el-form-item>
        <el-form-item label="Year">
          <el-input-number v-model="form.year" :min="1900" :max="2100" />
        </el-form-item>
        <el-form-item label="Capacity (kg)">
          <el-input-number v-model="form.capacity_kg" :min="0" />
        </el-form-item>
        <el-form-item label="Volume (m³)">
          <el-input-number v-model="form.volume_m3" :min="0" />
        </el-form-item>
        <el-form-item label="Truck Type">
          <el-input v-model="form.truck_type" />
        </el-form-item>
        <el-form-item label="GPS Enabled">
          <el-switch v-model="form.gps_enabled" />
        </el-form-item>
        <el-form-item label="Photo">
          <input type="file" @change="onFileChange" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible=false">Cancel</el-button>
        <el-button type="primary" @click="saveVehicle">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/layout/PageHeader/index.vue'
import { getVehicles, createVehicle, updateVehicle, deleteVehicleApi } from '@/api/api' // <-- täze API

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

async function fetchVehicles() {
  const { data } = await getVehicles()
  vehicles.value = data
}

function openDialog(vehicle?: Vehicle) {
  if (vehicle) {
    form.value = { ...vehicle }
  } else {
    form.value = { plate_number:'',brand:'',model:'',year:null,capacity_kg:0,volume_m3:0,truck_type:'',gps_enabled:false }
  }
  dialogVisible.value = true
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files?.length) file = target.files[0]
}

async function saveVehicle() {
  const formData = new FormData()
  Object.entries(form.value).forEach(([key, val]) => {
    if (val !== null && val !== undefined) formData.append(key, String(val))
  })
  if (file) formData.append('photo', file)

  if (form.value.id) {
    await updateVehicle(form.value.id, formData)
  } else {
    await createVehicle(formData)
  }
  dialogVisible.value = false
  await fetchVehicles()
}

async function deleteVehicle(id:number) {
  await deleteVehicleApi(id)
  await fetchVehicles()
}

onMounted(fetchVehicles)
</script>
