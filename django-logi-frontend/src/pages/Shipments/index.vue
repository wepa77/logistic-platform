<template>
  <div class="page">
    <PageHeader title="Shipments">
      <template #actions>
        <el-button type="primary" icon="Plus" @click="openDialog()">Add Shipment</el-button>
      </template>
    </PageHeader>

    <el-card shadow="hover" class="mt-4">
      <el-table :data="shipments" stripe border style="width: 100%">
        <el-table-column prop="cargo" label="Cargo">
          <template #default="{ row }">
            {{ row.cargo?.title || '—' }}
          </template>
        </el-table-column>
        <el-table-column prop="carrier" label="Carrier">
          <template #default="{ row }">
            {{ row.carrier?.username || '—' }}
          </template>
        </el-table-column>
        <el-table-column label="Payment" width="120">
          <template #default="{ row }">
            <el-tag
                :type="row.payment_status === 'paid'
                ? 'success'
                : row.payment_status === 'pending'
                ? 'warning'
                : 'danger'"
            >
              {{ row.payment_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="commission_amount" label="Commission" width="140">
          <template #default="{ row }">
            {{ row.commission_amount }} TMT
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="Start Time" width="180" />
        <el-table-column prop="end_time" label="End Time" width="180" />
        <el-table-column fixed="right" label="Actions" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">Edit</el-button>
            <el-popconfirm title="Delete this shipment?" @confirm="deleteShipment(row.id!)">
              <template #reference>
                <el-button size="small" type="danger">Delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog create/update -->
    <el-dialog v-model="dialogVisible" title="Shipment" width="600px">
      <el-form :model="form" label-width="150px">
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

        <el-form-item label="Carrier">
          <el-select v-model="form.carrier" placeholder="Select carrier" filterable style="width:100%">
            <el-option
                v-for="u in carrierOptions"
                :key="u.id"
                :label="u.username"
                :value="u.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Vehicle">
          <el-select v-model="form.vehicle" placeholder="Optional" filterable style="width:100%">
            <el-option
                v-for="v in vehicleOptions"
                :key="v.id"
                :label="`${v.plate_number} (${v.capacity_kg}kg)`"
                :value="v.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="Distance (km)">
          <el-input-number v-model="form.distance_km" :min="0" />
        </el-form-item>

        <el-form-item label="Total Price">
          <el-input-number v-model="form.total_price" :min="0" />
        </el-form-item>

        <el-form-item label="Payment Status">
          <el-select v-model="form.payment_status" placeholder="Select status">
            <el-option label="Paid" value="paid" />
            <el-option label="Pending" value="pending" />
            <el-option label="Failed" value="failed" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveShipment">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import PageHeader from '@/layout/PageHeader/index.vue'
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
  cargo: number | null
  carrier: number | null
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
const form = ref<Shipment>({
  cargo: null,
  carrier: null,
  vehicle: null,
  distance_km: null,
  total_price: null,
  payment_status: 'pending'
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
  if (shipment) form.value = { ...shipment }
  else
    form.value = {
      cargo: null,
      carrier: null,
      vehicle: null,
      distance_km: null,
      total_price: null,
      payment_status: 'pending'
    }
  dialogVisible.value = true
}

async function saveShipment() {
  if (form.value.id) {
    await apiUpdateShipment(form.value.id, form.value)
    ElMessage.success('Shipment updated')
  } else {
    await apiCreateShipment(form.value)
    ElMessage.success('Shipment created')
  }
  dialogVisible.value = false
  await fetchShipments()
}

async function deleteShipment(id: number) {
  await apiDeleteShipment(id)
  ElMessage.success('Shipment deleted')
  await fetchShipments()
}

onMounted(async () => {
  await fetchOptions()
  await fetchShipments()
})
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
</style>
