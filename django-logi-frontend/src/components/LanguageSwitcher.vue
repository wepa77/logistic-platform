<template>
  <div class="language-switcher">
    <el-button 
      text 
      :class="['language-btn', { active: locale === 'en' }]"
      @click="changeLanguage('en')"
    >
      <span class="flag">🇬🇧</span>
      <span class="language-text">EN</span>
    </el-button>
    
    <el-divider direction="vertical" border-style="dashed" />
    
    <el-button 
      text 
      :class="['language-btn', { active: locale === 'ru' }]"
      @click="changeLanguage('ru')"
    >
      <span class="flag">🇷🇺</span>
      <span class="language-text">RU</span>
    </el-button>
    
    <el-divider direction="vertical" border-style="dashed" />
    
    <el-button 
      text 
      :class="['language-btn', { active: locale === 'tk' }]"
      @click="changeLanguage('tk')"
    >
      <span class="flag">🇹🇲</span>
      <span class="language-text">TM</span>
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

// Current language label is now directly in the template

function changeLanguage(lang: string) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>

<style scoped>
.language-switcher {
  display: flex;
  align-items: center;
  height: 100%;
  margin: 0 8px;
}

.language-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
  height: 32px;
  min-width: 40px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
  border-radius: 4px;
  margin: 0 2px;
}

.language-btn:hover {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.language-btn.active {
  color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-8);
  font-weight: 600;
}

.language-text {
  margin-left: 4px;
  font-size: 13px;
}

.flag {
  font-size: 16px;
  line-height: 1;
}

:deep(.el-divider) {
  margin: 0 2px;
  height: 1em;
  background-color: var(--el-border-color);
}
</style>
