<template>
  <div class="page">
    <PageHeader title="Offers">
      <template #actions>
        <el-button type="primary" icon="Plus" @click="openDialog()">Add Offer</el-button>
      </template>
    </PageHeader>

    <el-card shadow="hover" class="mt-4">
      <el-table :data="offers" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="cargo" label="Cargo">
          <template #default="{ row }">
            <strong>{{ row.cargo?.title || '—' }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="carrier" label="Carrier">
          <template #default="{ row }">
            {{ row.carrier?.username || '—' }}
          </template>
        </el-table-column>
        <el-table-column prop="price" label="Price" width="120">
          <template #default="{ row }">
            {{ row.price }} TMT
          </template>
        </el-table-column>
        <el-table-column prop="status" label="Status" width="120">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="Actions" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">Edit</el-button>
            <el-popconfirm title="Delete this offer?" @confirm="deleteOffer(row.id!)">
              <template #reference>
                <el-button size="small" type="danger">Delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog for create/update -->
    <el-dialog v-model="dialogVisible" title="Offer" width="500px">
      <el-form :model="form" label-width="130px">
        <el-form-item label="Cargo">
          <el-select v-model="form.cargo" placeholder="Select cargo" filterable style="width:100%">
            <el-option
                v-for="c in cargoOptions"
                :key="c.id"
                :label="c.title"
                :value="c.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Price">
          <el-input-number v-model="form.price" :min="0" style="width:100%" />
        </el-form-item>
        <el-form-item label="Note">
          <el-input v-model="form.note" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="Vehicle">
          <el-select v-model="form.vehicle" placeholder="Select vehicle" filterable style="width:100%">
            <el-option
                v-for="v in vehicleOptions"
                :key="v.id"
                :label="`${v.plate_number} (${v.capacity_kg}kg)`"
                :value="v.id"
            />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveOffer">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/layout/PageHeader/index.vue'
import { ElMessage } from 'element-plus'
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
  cargo: number | null
  carrier?: { id: number; username: string }
  price: number
  note?: string
  status?: string
  vehicle?: number | null
}

interface CargoOption {
  id: number
  title: string
}

interface VehicleOption {
  id: number
  plate_number: string
  capacity_kg: number
}

const offers = ref<Offer[]>([])
const cargoOptions = ref<CargoOption[]>([])
const vehicleOptions = ref<VehicleOption[]>([])
const dialogVisible = ref(false)
const form = ref<Offer>({ cargo: null, price: 0, note: '', vehicle: null })

function statusType(status?: string) {
  if (status === 'accepted') return 'success'
  if (status === 'rejected') return 'danger'
  return 'info'
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
  if (offer) form.value = { ...offer }
  else form.value = { cargo: null, price: 0, note: '', vehicle: null }
  dialogVisible.value = true
}

async function saveOffer() {
  if (form.value.id) {
    await apiUpdateOffer(form.value.id, form.value)
    ElMessage.success('Offer updated')
  } else {
    await apiCreateOffer(form.value)
    ElMessage.success('Offer created')
  }
  dialogVisible.value = false
  await fetchOffers()
}

async function deleteOffer(id: number) {
  await apiDeleteOffer(id)
  ElMessage.success('Offer deleted')
  await fetchOffers()
}

onMounted(async () => {
  await fetchOptions()
  await fetchOffers()
})
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
</style>
