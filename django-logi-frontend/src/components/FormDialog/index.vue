<template>
  <el-dialog v-model="open" :title="title" width="520px" destroy-on-close>
    <slot></slot>
    <template #footer>
      <el-space>
        <el-button @click="open=false">Cancel</el-button>
        <el-button type="primary" @click="$emit('submit')">Save</el-button>
      </el-space>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
const open = defineModel<boolean>('open', { required: true })
defineProps<{ title:string }>()
defineEmits<{ (e:'submit'):void }>()
</script>
