<template>
  <ul class="quick-stats">
    <li>
      <i class="mdi mdi-package-variant-closed"></i>
      <span>{{ formatNumber(cargos) }} {{ $t ? $t('home.cargosLabel') : defaultLabels.cargos }}</span>
    </li>
    <li>
      <i class="mdi mdi-truck"></i>
      <span>{{ formatNumber(vehicles) }} {{ $t ? $t('home.vehiclesLabel') : defaultLabels.vehicles }}</span>
    </li>
    <li>
      <i class="mdi mdi-account-group"></i>
      <span>{{ formatNumber(users) }} {{ $t ? $t('home.usersLabel') : defaultLabels.users }}</span>
    </li>
    <li>
      <i class="mdi mdi-file-document-outline"></i>
      <span>{{ formatNumber(tenders) }} {{ $t ? $t('home.tendersLabel') : defaultLabels.tenders }}</span>
    </li>
  </ul>
</template>

<script lang="ts" setup>
import { withDefaults, defineProps } from 'vue'

interface Props {
  cargos?: number
  vehicles?: number
  users?: number
  tenders?: number
  labels?: {
    cargos?: string
    vehicles?: string
    users?: string
    tenders?: string
  }
}

withDefaults(defineProps<Props>(), {
  cargos: 183544,
  vehicles: 74978,
  users: 466302,
  tenders: 192,
  labels: () => ({})
})

// local i18n-safe fallback labels
const defaultLabels = {
  cargos: 'грузов',
  vehicles: 'машин',
  users: 'участников',
  tenders: 'тендера'
}

function formatNumber(n?: number) {
  if (typeof n !== 'number') return ''
  return new Intl.NumberFormat().format(n)
}
</script>

<style scoped>
.quick-stats {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 0;
  margin: 0;
  list-style: none;
  color: #1f2937;
}

.quick-stats li { display: flex; align-items: center; gap: 8px; }
.quick-stats i { color: #0f766e; }

@media (min-width: 1024px) {
  .quick-stats { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
</style>
