<template>
  <div>
    <div class="mb-2"><slot name="actions"></slot></div>
    <el-table :data="rows" stripe border @selection-change="onSel"><el-table-column type="selection" width="45"/><slot /></el-table>
    <div class="mt-2 flex justify-end">
      <el-pagination layout="prev, pager, next" :page-size="pageSize" :total="total" @current-change="$emit('page', $event)" />
    </div>
  </div>
</template>
<script setup lang="ts">
defineProps<{ rows:any[]; total:number; pageSize?:number }>()
const emit = defineEmits<{ (e:'selection', val:any[]):void; (e:'page', p:number):void }>()
const onSel = (val:any[]) => emit('selection', val)
</script>
<style scoped>
.mb-2{margin-bottom:.5rem}.mt-2{margin-top:.5rem}.flex{display:flex}.justify-end{justify-content:flex-end}
</style>
