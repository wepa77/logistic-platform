<template>
  <div class="page">
    <PageHeader title="Reviews">
      <template #actions>
        <el-button type="primary" icon="Plus" @click="openDialog()">
          Add Review
        </el-button>
      </template>
    </PageHeader>

    <el-card shadow="hover" class="mt-4">
      <el-table :data="reviews" stripe border style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="shipment" label="Shipment">
          <template #default="{ row }">
            {{ row.shipment?.cargo?.title || '—' }}
          </template>
        </el-table-column>
        <el-table-column prop="reviewer" label="Reviewer">
          <template #default="{ row }">
            {{ row.reviewer?.username || '—' }}
          </template>
        </el-table-column>
        <el-table-column prop="rating" label="Rating" width="120">
          <template #default="{ row }">
            <el-rate :model-value="row.rating" disabled />
          </template>
        </el-table-column>
        <el-table-column prop="comment" label="Comment" />
        <el-table-column prop="created_at" label="Created" width="180" />
        <el-table-column fixed="right" label="Actions" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">Edit</el-button>
            <el-popconfirm title="Delete this review?" @confirm="deleteReview(row.id!)">
              <template #reference>
                <el-button size="small" type="danger">Delete</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Dialog create / edit -->
    <el-dialog v-model="dialogVisible" title="Review" width="500px">
      <el-form :model="form" label-width="120px">
        <el-form-item label="Shipment">
          <el-select v-model="form.shipment" placeholder="Select shipment" filterable style="width:100%">
            <el-option
                v-for="s in shipmentOptions"
                :key="s.id"
                :label="s.cargo?.title || `Shipment #${s.id}`"
                :value="s.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Rating">
          <el-rate v-model="form.rating" />
        </el-form-item>
        <el-form-item label="Comment">
          <el-input v-model="form.comment" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="saveReview">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import PageHeader from '@/layout/PageHeader/index.vue'
import { ElMessage } from 'element-plus'
import {
  getReviews as apiGetReviews,
  createReview as apiCreateReview,
  updateReview as apiUpdateReview,
  deleteReview as apiDeleteReview,
  getShipments as apiGetShipments
} from '@/api/api'

interface Review {
  id?: number
  shipment: number | null
  reviewer?: { id: number; username: string }
  rating: number
  comment?: string
  created_at?: string
}

const reviews = ref<Review[]>([])
const shipmentOptions = ref<any[]>([])
const dialogVisible = ref(false)
const form = ref<Review>({ shipment: null, rating: 0, comment: '' })

async function fetchReviews() {
  const { data } = await apiGetReviews()
  reviews.value = data
}

async function fetchShipments() {
  const { data } = await apiGetShipments()
  shipmentOptions.value = data
}

function openDialog(review?: Review) {
  if (review) form.value = { ...review }
  else form.value = { shipment: null, rating: 0, comment: '' }
  dialogVisible.value = true
}

async function saveReview() {
  if (form.value.id) {
    await apiUpdateReview(form.value.id, form.value)
    ElMessage.success('Review updated')
  } else {
    await apiCreateReview(form.value)
    ElMessage.success('Review created')
  }
  dialogVisible.value = false
  await fetchReviews()
}

async function deleteReview(id: number) {
  await apiDeleteReview(id)
  ElMessage.success('Review deleted')
  await fetchReviews()
}

onMounted(async () => {
  await fetchShipments()
  await fetchReviews()
})
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
</style>
