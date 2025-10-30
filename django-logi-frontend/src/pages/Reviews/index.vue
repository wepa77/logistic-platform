<template>
  <div class="reviews-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-star-outline"></i>
            Reviews & Ratings
          </h1>
          <p class="page-subtitle">Manage customer feedback and service ratings</p>
        </div>
        <div class="header-actions">
          <el-button type="primary" size="large" @click="openDialog()" class="add-btn">
            <i class="mdi mdi-plus"></i>
            Add Review
          </el-button>
        </div>
      </div>
    </div>

    <!-- Filters & Search Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            placeholder="Search by reviewer, shipment..."
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="ratingFilter" placeholder="Filter by Rating" clearable class="rating-filter">
          <el-option label="All Ratings" value="" />
          <el-option label="5 Stars" :value="5" />
          <el-option label="4 Stars" :value="4" />
          <el-option label="3 Stars" :value="3" />
          <el-option label="2 Stars" :value="2" />
          <el-option label="1 Star" :value="1" />
        </el-select>

        <el-button class="filter-btn" @click="fetchReviews">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="mdi mdi-comment-multiple-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ reviews.length }}</div>
          <div class="stat-label">Total Reviews</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon average">
          <i class="mdi mdi-star"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.averageRating.toFixed(1) }}</div>
          <div class="stat-label">Average Rating</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon excellent">
          <i class="mdi mdi-star-check"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.fiveStars }}</div>
          <div class="stat-label">5-Star Reviews</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon recent">
          <i class="mdi mdi-clock-outline"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.recentReviews }}</div>
          <div class="stat-label">This Month</div>
        </div>
      </div>
    </div>

    <!-- Reviews Table -->
    <el-card class="table-card" shadow="never">
      <el-table :data="filteredReviews" style="width: 100%" class="modern-table">
        <el-table-column label="Shipment" min-width="200">
          <template #default="{ row }">
            <div class="shipment-cell">
              <i class="mdi mdi-package-variant-closed"></i>
              <span>{{ row.shipment?.cargo?.title || 'N/A' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Reviewer" min-width="180">
          <template #default="{ row }">
            <div class="reviewer-cell">
              <el-avatar :size="32" class="reviewer-avatar">
                <i class="mdi mdi-account"></i>
              </el-avatar>
              <span>{{ row.reviewer?.username || 'Anonymous' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Rating" width="180">
          <template #default="{ row }">
            <div class="rating-cell">
              <el-rate :model-value="row.rating" disabled size="large" />
              <span class="rating-number">{{ row.rating }}/5</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Comment" min-width="300">
          <template #default="{ row }">
            <div class="comment-cell">
              <i class="mdi mdi-comment-text-outline"></i>
              <span>{{ row.comment || 'No comment provided' }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="Date" width="160">
          <template #default="{ row }">
            <div class="date-cell">
              <i class="mdi mdi-calendar"></i>
              <span>{{ formatDate(row.created_at) }}</span>
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
                  title="Are you sure to delete this review?"
                  @confirm="deleteReview(row.id!)"
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

    <!-- Modern Dialog for create/edit -->
    <el-dialog
        v-model="dialogVisible"
        :title="form.id ? 'Edit Review' : 'Add New Review'"
        width="600px"
        class="modern-dialog"
    >
      <el-form :model="form" label-position="top" class="review-form">
        <el-form-item label="Shipment">
          <el-select v-model="form.shipment" placeholder="Select shipment" filterable style="width:100%">
            <el-option
                v-for="s in shipmentOptions"
                :key="s.id"
                :label="s.cargo?.title || `Shipment #${s.id}`"
                :value="s.id"
            >
              <div class="option-item">
                <i class="mdi mdi-package-variant-closed"></i>
                <span>{{ s.cargo?.title || `Shipment #${s.id}` }}</span>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="Rating">
          <div class="rating-input">
            <el-rate v-model="form.rating" size="large" show-text />
            <span class="rating-label">{{ ratingLabel(form.rating) }}</span>
          </div>
        </el-form-item>

        <el-form-item label="Comment">
          <el-input
              v-model="form.comment"
              type="textarea"
              :rows="4"
              placeholder="Share your experience..."
              maxlength="500"
              show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button size="large" @click="dialogVisible = false">
            <i class="mdi mdi-close"></i>
            Cancel
          </el-button>
          <el-button type="primary" size="large" @click="saveReview">
            <i class="mdi mdi-check"></i>
            {{ form.id ? 'Update' : 'Submit' }} Review
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
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
  shipment: any
  reviewer?: { id: number; username: string }
  rating: number
  comment?: string
  created_at?: string
}

const reviews = ref<Review[]>([])
const shipmentOptions = ref<any[]>([])
const dialogVisible = ref(false)
const searchQuery = ref('')
const ratingFilter = ref<number | ''>()

const form = ref<Review>({ shipment: null, rating: 0, comment: '' })

// Computed stats
const stats = computed(() => {
  const total = reviews.value.length
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  const fiveStars = reviews.value.filter(r => r.rating === 5).length
  
  // Reviews from this month
  const now = new Date()
  const thisMonth = reviews.value.filter(r => {
    if (!r.created_at) return false
    const date = new Date(r.created_at)
    return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear()
  }).length

  return {
    averageRating: total > 0 ? sum / total : 0,
    fiveStars,
    recentReviews: thisMonth,
  }
})

// Filtered reviews
const filteredReviews = computed(() => {
  let filtered = reviews.value

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(review =>
      review.reviewer?.username?.toLowerCase().includes(query) ||
      review.shipment?.cargo?.title?.toLowerCase().includes(query) ||
      review.comment?.toLowerCase().includes(query)
    )
  }

  // Filter by rating
  if (ratingFilter.value) {
    filtered = filtered.filter(review => review.rating === ratingFilter.value)
  }

  return filtered
})

async function fetchReviews() {
  const { data } = await apiGetReviews()
  reviews.value = data
}

async function fetchShipments() {
  const { data } = await apiGetShipments()
  shipmentOptions.value = data
}

function openDialog(review?: Review) {
  if (review) {
    form.value = {
      ...review,
      shipment: review.shipment?.id || review.shipment
    }
  } else {
    form.value = { shipment: null, rating: 0, comment: '' }
  }
  dialogVisible.value = true
}

async function saveReview() {
  if (form.value.id) {
    await apiUpdateReview(form.value.id, form.value)
    ElMessage.success('Review updated successfully')
  } else {
    await apiCreateReview(form.value)
    ElMessage.success('Review submitted successfully')
  }
  dialogVisible.value = false
  await fetchReviews()
}

async function deleteReview(id: number) {
  await apiDeleteReview(id)
  ElMessage.success('Review deleted successfully')
  await fetchReviews()
}

function ratingLabel(rating: number) {
  const labels = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
  return labels[rating] || ''
}

function formatDate(date: string) {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(async () => {
  await fetchShipments()
  await fetchReviews()
})
</script>

<style scoped>
.reviews-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 12px;
}

/* ---------------- PAGE HEADER ---------------- */
.page-header {
  margin-bottom: 24px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #3b82f6;
  font-size: 32px;
}

/* ---------------- FILTERS ---------------- */
.filters-card {
  margin-bottom: 20px;
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

.rating-filter {
  width: 180px;
}

/* ---------------- STATS ---------------- */
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
}

/* ---------------- TABLE ---------------- */
.table-card {
  border-radius: 12px;
}

.modern-table {
  border-radius: 8px;
  overflow: auto; /* ✅ Horizontal scroll for mobile */
}

.shipment-cell,
.reviewer-cell,
.comment-cell,
.date-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* ---------------- DIALOG ---------------- */
.modern-dialog :deep(.el-dialog) {
  border-radius: 16px;
}

/* ---------------- RESPONSIVE ---------------- */

/* ✅ 1024px — Laptop & Tablet */
@media (max-width: 1024px) {
  .page-title {
    font-size: 24px;
  }

  .page-header {
    margin-bottom: 18px;
  }

  .filters-container {
    flex-wrap: wrap;
  }

  .rating-filter {
    width: 200px;
  }
}

/* ✅ 900px — Collapse Stats to 2 columns */
@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* ✅ 768px — Mobile Layout */
@media (max-width: 768px) {
  .page-title {
    font-size: 22px;
  }

  .filters-container {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input,
  .rating-filter {
    width: 100%;
    max-width: none;
  }

  .stat-card {
    padding: 16px;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .modern-table {
    font-size: 14px;
  }

  .modern-dialog :deep(.el-dialog) {
    width: 90% !important;
  }
}

/* ✅ 600px — Phones */
@media (max-width: 600px) {
  .page-title {
    font-size: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr; /* ✅ 1-per-row */
  }

  .rating-cell {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-buttons {
    justify-content: center;
  }

  .comment-cell {
    font-size: 13px;
  }
}

/* ✅ 480px — Small phones */
@media (max-width: 480px) {
  .page-title {
    font-size: 18px;
  }

  .stat-value {
    font-size: 22px;
  }

  .modern-table {
    font-size: 13px;
  }

  .filters-card {
    padding: 12px;
  }
}

/* ✅ 360px — Ultra small devices */
@media (max-width: 360px) {
  .page-title {
    font-size: 16px;
  }

  .stat-card {
    padding: 12px;
  }

  .add-btn {
    font-size: 14px;
    padding: 10px 16px;
  }

  .comment-cell {
    font-size: 12px;
  }
}

</style>
