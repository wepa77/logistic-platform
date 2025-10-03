<template>
  <div class="page">
    <PageHeader title="Wallet">
      <template #actions>
        <el-tag effect="plain" type="success" size="large">
          💳 Balance: <b>{{ balance || 0 }} TMT</b>
        </el-tag>
      </template>
    </PageHeader>

    <!-- Top-up card -->
    <el-card shadow="hover" class="mt-4">
      <div class="topup-bar">
        <el-input-number
            v-model="amount"
            :min="1"
            label="Top-up amount"
            :precision="2"
            placeholder="Amount"
        />
        <el-button type="primary" icon="Coin" @click="handleTopup" :loading="loading">
          Add Balance
        </el-button>
      </div>
    </el-card>

    <!-- Transactions -->
    <el-card shadow="hover" class="mt-4">
      <h3 class="mb-2">Recent Transactions</h3>
      <el-table :data="transactions" stripe border>
        <el-table-column prop="created_at" label="Date" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="tx_type" label="Type" width="150">
          <template #default="{ row }">
            <el-tag :type="typeColor(row.tx_type)">
              {{ row.tx_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="Amount" width="120">
          <template #default="{ row }">
            <span :class="row.amount >= 0 ? 'positive' : 'negative'">
              {{ row.amount }} TMT
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="Description" min-width="250" />
        <el-table-column prop="success" label="Status" width="100">
          <template #default="{ row }">
            <el-tag :type="row.success ? 'success' : 'danger'">
              {{ row.success ? 'Success' : 'Failed' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import PageHeader from "@/layout/PageHeader/index.vue";
import { ElMessage } from "element-plus";
import { getBalance, getWalletTransactions, createTopUp } from "@/api/api";

interface WalletTx {
  id: number;
  created_at: string;
  tx_type: string;
  amount: number;
  description: string;
  success: boolean;
}

const balance = ref<number>(0);
const amount = ref<number>(50);
const transactions = ref<WalletTx[]>([]);
const loading = ref(false);

async function fetchWallet() {
  const { data: bal } = await getBalance();
  balance.value = Number(bal.balance) || 0;

  const { data: tx } = await getWalletTransactions();
  transactions.value = tx;
}

async function handleTopup() {
  if (!amount.value || amount.value <= 0) {
    return ElMessage.warning("Enter top-up amount");
  }
  loading.value = true;
  try {
    await createTopUp({ amount: amount.value });
    ElMessage.success("Top-up created successfully");
    await fetchWallet();
  } catch (err) {
    console.error(err);
    ElMessage.error("Failed to create top-up");
  } finally {
    loading.value = false;
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleString();
}

function typeColor(type: string) {
  switch (type) {
    case "topup":
      return "success";
    case "commission":
      return "warning";
    default:
      return "info";
  }
}

onMounted(fetchWallet);
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
.topup-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}
.positive {
  color: #16a34a;
  font-weight: 600;
}
.negative {
  color: #dc2626;
  font-weight: 600;
}
.mb-2 {
  margin-bottom: 0.75rem;
}
</style>
