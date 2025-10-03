<template>
  <div class="page-header">
    <div class="page-title">
      <h2>{{ title }}</h2>
    </div>
    <div class="page-actions">
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.page-title h2 {
  font-size: 1.5rem;
  margin: 0;
}

.page-actions {
  display: flex;
  gap: 0.5rem;
}
</style>
