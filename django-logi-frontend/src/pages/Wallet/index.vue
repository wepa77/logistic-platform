<template>
  <div class="wallet-page">
    <!-- Header Section -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-left">
          <h1 class="page-title">
            <i class="mdi mdi-wallet-outline"></i>
            {{ $t('wallet.title') }}
          </h1>
          <p class="page-subtitle">{{ $t('wallet.subtitle') }}</p>
        </div>
      </div>
    </div>

    <!-- Balance & Stats Cards -->
    <div class="stats-grid">
      <div class="balance-card">
        <div class="balance-icon">
          <i class="mdi mdi-wallet"></i>
        </div>
        <div class="balance-content">
          <div class="balance-label">{{ $t('wallet.currentBalance') }}</div>
          <div class="balance-value">{{ balance.toFixed(2) }} TMT</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon income">
          <i class="mdi mdi-arrow-down-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalIncome.toFixed(2) }}</div>
          <div class="stat-label">{{ $t('wallet.totalIncome') }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon expense">
          <i class="mdi mdi-arrow-up-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ Math.abs(stats.totalExpense).toFixed(2) }}</div>
          <div class="stat-label">{{ $t('wallet.totalExpense') }}</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon transactions">
          <i class="mdi mdi-swap-horizontal"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ transactions.length }}</div>
          <div class="stat-label">{{ $t('wallet.transactions') }}</div>
        </div>
      </div>
    </div>

    <!-- Top-up Card -->
    <el-card class="topup-card" shadow="never">
      <div class="topup-header">
        <div class="topup-title">
          <i class="mdi mdi-cash-plus"></i>
          <span>{{ $t('wallet.addBalance') }}</span>
        </div>
        <p class="topup-subtitle">{{ $t('wallet.topUp') }}</p>
      </div>
      <div class="topup-content">
        <div class="amount-input-wrapper">
          <label class="input-label">{{ $t('wallet.amount') }}</label>
          <el-input-number
              v-model="amount"
              :min="1"
              :precision="2"
              :step="10"
              size="large"
              class="amount-input"
          />
        </div>
        <div class="quick-amounts">
          <button 
              v-for="quickAmount in [50, 100, 200, 500]" 
              :key="quickAmount"
              @click="amount = quickAmount"
              class="quick-amount-btn"
              :class="{ active: amount === quickAmount }"
          >
            {{ quickAmount }} TMT
          </button>
        </div>
        <el-button 
            type="primary" 
            size="large" 
            @click="handleTopup" 
            :loading="loading"
            class="topup-btn"
        >
          <i class="mdi mdi-plus-circle"></i>
          {{ $t('wallet.addAmountToBalance', { amount }) }}
        </el-button>
      </div>
    </el-card>

    <!-- Filters Section -->
    <el-card class="filters-card" shadow="never">
      <div class="filters-container">
        <el-input
            v-model="searchQuery"
            :placeholder="$t('wallet.searchPlaceholder')"
            class="search-input"
            clearable
        >
          <template #prefix>
            <i class="mdi mdi-magnify"></i>
          </template>
        </el-input>

        <el-select v-model="typeFilter" :placeholder="$t('wallet.filterByType')" clearable class="type-filter">
          <el-option :label="$t('wallet.allTypes')" value="" />
          <el-option :label="$t('wallet.topup')" value="topup" />
          <el-option :label="$t('wallet.commission')" value="commission" />
          <el-option :label="$t('wallet.payment')" value="payment" />
        </el-select>

        <el-select v-model="statusFilter" :placeholder="$t('wallet.filterByStatus')" clearable class="status-filter">
          <el-option :label="$t('wallet.allStatus')" value="" />
          <el-option :label="$t('wallet.success')" value="success" />
          <el-option :label="$t('wallet.failed')" value="failed" />
        </el-select>

        <el-button class="filter-btn" @click="fetchWallet">
          <i class="mdi mdi-refresh"></i>
        </el-button>
      </div>
    </el-card>

    <!-- Transactions Table -->
    <el-card class="table-card" shadow="never">
      <div class="table-header">
        <h3 class="table-title">
          <i class="mdi mdi-history"></i>
          {{ $t('wallet.transactionHistory') }}
        </h3>
        <el-button text class="export-btn">
          <i class="mdi mdi-download"></i>
          {{ $t('common.export') }}
        </el-button>
      </div>

      <el-table :data="filteredTransactions" style="width: 100%" class="modern-table">
        <el-table-column prop="created_at" :label="$t('wallet.dateTime')" width="200">
          <template #default="{ row }">
            <div class="date-cell">
              <i class="mdi mdi-calendar-clock"></i>
              <span>{{ formatDate(row.created_at) }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="tx_type" :label="$t('wallet.type')" width="150">
          <template #default="{ row }">
            <el-tag 
                :type="typeColor(row.tx_type)"
                :class="`tx-type-tag tx-${row.tx_type}`"
                effect="plain"
            >
              <i :class="typeIcon(row.tx_type)"></i>
              {{ formatType(row.tx_type) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="amount" :label="$t('wallet.amount')" width="160">
          <template #default="{ row }">
            <div class="amount-cell" :class="row.amount >= 0 ? 'positive' : 'negative'">
              <i :class="row.amount >= 0 ? 'mdi mdi-plus-circle' : 'mdi mdi-minus-circle'"></i>
              <span>{{ row.amount >= 0 ? '+' : '' }}{{ row.amount.toFixed(2) }} TMT</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="description" :label="$t('wallet.description')" min-width="250">
          <template #default="{ row }">
            <div class="description-cell">
              {{ row.description || $t('wallet.noDescription') }}
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="success" :label="$t('common.status')" width="120">
          <template #default="{ row }">
            <el-tag 
                :type="row.success ? 'success' : 'danger'"
                :class="`status-tag status-${row.success ? 'success' : 'failed'}`"
                effect="plain"
            >
              <i :class="row.success ? 'mdi mdi-check-circle' : 'mdi mdi-close-circle'"></i>
              {{ row.success ? $t('wallet.success') : $t('wallet.failed') }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="filteredTransactions.length === 0" class="empty-state">
        <i class="mdi mdi-inbox-outline"></i>
        <p>{{ $t('wallet.noTransactions') }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { ElMessage } from "element-plus";
import { getBalance, getWalletTransactions, createTopUp } from "@/api/api";
import { useI18n } from 'vue-i18n'

interface WalletTx {
  id: number;
  created_at: string;
  tx_type: string;
  amount: number;
  description: string;
  success: boolean;
}

const { t, locale } = useI18n()

const balance = ref<number>(0);
const amount = ref<number>(50);
const transactions = ref<WalletTx[]>([]);
const loading = ref(false);
const searchQuery = ref('');
const typeFilter = ref('');
const statusFilter = ref('');

// Computed stats
const stats = computed(() => {
  const income = transactions.value
    .filter(tx => tx.amount > 0 && tx.success)
    .reduce((sum, tx) => sum + tx.amount, 0);
  
  const expense = transactions.value
    .filter(tx => tx.amount < 0 && tx.success)
    .reduce((sum, tx) => sum + tx.amount, 0);

  return {
    totalIncome: income,
    totalExpense: expense,
  };
});

// Filtered transactions
const filteredTransactions = computed(() => {
  let filtered = transactions.value;

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(tx =>
      tx.description?.toLowerCase().includes(query) ||
      tx.tx_type.toLowerCase().includes(query)
    );
  }

  // Filter by type
  if (typeFilter.value) {
    filtered = filtered.filter(tx => tx.tx_type === typeFilter.value);
  }

  // Filter by status
  if (statusFilter.value) {
    const isSuccess = statusFilter.value === 'success';
    filtered = filtered.filter(tx => tx.success === isSuccess);
  }

  return filtered;
});

async function fetchWallet() {
  const { data: bal } = await getBalance();
  balance.value = Number(bal.balance) || 0;

  const { data: tx } = await getWalletTransactions();
  transactions.value = tx;
}

async function handleTopup() {
  if (!amount.value || amount.value <= 0) {
    return ElMessage.warning(t('wallet.enterTopupAmount'));
  }
  loading.value = true;
  try {
    await createTopUp({ amount: amount.value });
    ElMessage.success(t('wallet.topupCreated'));
    await fetchWallet();
  } catch (err) {
    console.error(err);
    ElMessage.error(t('wallet.topupFailed'));
  } finally {
    loading.value = false;
  }
}

function formatDate(date: string) {
  const loc = (locale?.value as unknown as string) || 'en-US'
  return new Date(date).toLocaleString(loc, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function typeColor(type: string) {
  switch (type) {
    case "topup":
      return "success";
    case "commission":
      return "warning";
    case "payment":
      return "info";
    default:
      return "info";
  }
}

function typeIcon(type: string) {
  switch (type) {
    case "topup":
      return "mdi mdi-cash-plus";
    case "commission":
      return "mdi mdi-percent";
    case "payment":
      return "mdi mdi-credit-card";
    default:
      return "mdi mdi-swap-horizontal";
  }
}

function formatType(type: string) {
  switch (type) {
    case 'topup':
      return t('wallet.topup')
    case 'commission':
      return t('wallet.commission')
    case 'payment':
      return t('wallet.payment')
    default:
      return type
  }
}

onMounted(fetchWallet);
</script>

<style scoped>
.wallet-page {
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

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.balance-card {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
  transition: all 0.3s ease;
  grid-column: span 1;
}

.balance-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
}

.balance-icon {
  width: 64px;
  height: 64px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  color: white;
  backdrop-filter: blur(10px);
}

.balance-content {
  flex: 1;
}

.balance-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.balance-value {
  font-size: 32px;
  font-weight: 700;
  color: white;
  line-height: 1;
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

.stat-icon.income {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.stat-icon.expense {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.stat-icon.transactions {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
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

/* Top-up Card */
.topup-card {
  margin-bottom: 20px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.topup-header {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.topup-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 6px;
}

.topup-title i {
  color: #3b82f6;
  font-size: 24px;
}

.topup-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
}

.topup-content {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.amount-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.amount-input {
  width: 100%;
  max-width: 300px;
}

.quick-amounts {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-amount-btn {
  padding: 10px 20px;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quick-amount-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.quick-amount-btn.active {
  border-color: #3b82f6;
  background: #3b82f6;
  color: white;
}

.topup-btn {
  align-self: flex-start;
  padding: 12px 32px;
  font-weight: 600;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.topup-btn i {
  margin-right: 8px;
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
.status-filter {
  width: 180px;
}

.filter-btn {
  padding: 12px;
  font-size: 20px;
  border-radius: 8px;
}

/* Table Card */
.table-card {
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.table-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-title i {
  color: #3b82f6;
  font-size: 22px;
}

.export-btn {
  font-weight: 600;
  color: #64748b;
}

.export-btn i {
  margin-right: 6px;
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

.date-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
}

.date-cell i {
  color: #94a3b8;
  font-size: 16px;
}

.tx-type-tag {
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.tx-type-tag i {
  font-size: 14px;
}

.amount-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 700;
  font-size: 15px;
}

.amount-cell i {
  font-size: 18px;
}

.amount-cell.positive {
  color: #10b981;
}

.amount-cell.negative {
  color: #ef4444;
}

.description-cell {
  color: #64748b;
  font-size: 14px;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filters-container {
    flex-direction: column;
  }

  .search-input,
  .type-filter,
  .status-filter {
    width: 100%;
    max-width: none;
  }

  .quick-amounts {
    justify-content: stretch;
  }

  .quick-amount-btn {
    flex: 1;
  }

  .topup-btn {
    width: 100%;
  }
}
</style>
