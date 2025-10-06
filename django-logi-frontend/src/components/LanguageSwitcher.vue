<template>
  <el-dropdown trigger="click" @command="changeLanguage">
    <el-button text class="language-btn">
      <i class="mdi mdi-translate"></i>
      <span class="language-text">{{ currentLanguageLabel }}</span>
      <i class="mdi mdi-chevron-down"></i>
    </el-button>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="en" :class="{ active: locale === 'en' }">
          <div class="language-option">
            <span class="flag">🇬🇧</span>
            <span>English</span>
          </div>
        </el-dropdown-item>
        <el-dropdown-item command="ru" :class="{ active: locale === 'ru' }">
          <div class="language-option">
            <span class="flag">🇷🇺</span>
            <span>Русский</span>
          </div>
        </el-dropdown-item>
        <el-dropdown-item command="tk" :class="{ active: locale === 'tk' }">
          <div class="language-option">
            <span class="flag">🇹🇲</span>
            <span>Türkmençe</span>
          </div>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const currentLanguageLabel = computed(() => {
  const labels: Record<string, string> = {
    en: 'EN',
    ru: 'RU',
    tk: 'TM'
  }
  return labels[locale.value] || 'EN'
})

function changeLanguage(lang: string) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>

<style scoped>
.language-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  color: #94a3b8;
  font-weight: 500;
  transition: all 0.3s ease;
}

.language-btn:hover {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
}

.language-text {
  font-size: 14px;
  font-weight: 600;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
}

.flag {
  font-size: 18px;
}

.el-dropdown-menu__item.active {
  background: #eff6ff;
  color: #3b82f6;
  font-weight: 600;
}
</style>
