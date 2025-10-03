<template>
  <div class="page">
    <PageHeader title="Cargos">
      <template #actions>
        <el-button type="primary" icon="Plus" @click="openDialog()">Add Cargo</el-button>
      </template>
    </PageHeader>

    <!-- Cargos table -->
    <el-card shadow="hover" class="mt-4">
      <el-table :data="cargos" stripe border style="width: 100%">
        <el-table-column prop="title" label="Title" />
        <el-table-column prop="weight_kg" label="Weight (kg)" width="120" />
        <el-table-column prop="pickup_address" label="Pickup" />
        <el-table-column prop="delivery_address" label="Delivery" />
        <el-table-column prop="pickup_date" label="Pickup Date" width="140" />
        <el-table-column prop="status" label="Status" width="120">
          <template #default="scope">
            <el-tag
                :type="statusTag(scope.row.status)"
                effect="light"
                disable-transitions
            >
              {{ scope.row.status }}
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
                title="Delete this cargo?"
                @confirm="deleteCargo(scope.row.id)"
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
    <el-dialog v-model="dialogVisible" title="Cargo" width="600px">
      <el-form :model="form" label-width="130px">
        <el-form-item label="Title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="Description">
          <el-input v-model="form.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="Weight (kg)">
          <el-input-number v-model="form.weight_kg" :min="0" />
        </el-form-item>
        <el-form-item label="Volume (m³)">
          <el-input-number v-model="form.volume_m3" :min="0" />
        </el-form-item>
        <el-form-item label="Pickup Address">
          <el-input v-model="form.pickup_address" />
        </el-form-item>
        <el-form-item label="Delivery Address">
          <el-input v-model="form.delivery_address" />
        </el-form-item>
        <el-form-item label="Pickup Date">
          <el-date-picker
              v-model="form.pickup_date"
              type="date"
              placeholder="Select date"
              style="width:100%"
          />
        </el-form-item>
        <el-form-item label="Delivery Date">
          <el-date-picker
              v-model="form.delivery_date"
              type="date"
              placeholder="Optional"
              style="width:100%"
          />
        </el-form-item>
        <el-form-item label="Price Offer">
          <el-input-number v-model="form.price_offer" :min="0" />
        </el-form-item>
        <el-form-item label="Photo">
          <input type="file" @change="onFileChange" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveCargo">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/layout/PageHeader/index.vue'
import { ElMessage } from 'element-plus'

// ✅ dogry import — ähli API funksiýalary täze `api.ts`-dan
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
  dialogVisible.value = true
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files?.length) file = target.files[0]
}

async function saveCargo() {
  const formData = new FormData()
  Object.entries(form.value).forEach(([key, val]) => {
    if (val !== null && val !== undefined) formData.append(key, String(val))
  })
  if (file) formData.append('photo', file)

  if (form.value.id) {
    await apiUpdateCargo(form.value.id, formData)
    ElMessage.success('Cargo updated')
  } else {
    await apiCreateCargo(formData)
    ElMessage.success('Cargo created')
  }
  dialogVisible.value = false
  await fetchCargos()
}

async function deleteCargo(id: number) {
  await apiDeleteCargo(id)
  ElMessage.success('Cargo deleted')
  await fetchCargos()
}

onMounted(fetchCargos)
</script>

