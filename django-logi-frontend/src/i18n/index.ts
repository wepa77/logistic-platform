import { createI18n } from 'vue-i18n'
import en from './locales/en'
import ru from './locales/ru'
import tk from './locales/tk'

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    ru,
    tk
  }
})

export default i18n
