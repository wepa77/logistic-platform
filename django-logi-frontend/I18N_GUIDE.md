# Multi-Language Implementation Guide

## Overview
Your logistics platform now supports 3 languages:
- 🇬🇧 English (en)
- 🇷🇺 Russian (ru)
- 🇹🇲 Turkmen (tk)

## What's Been Implemented

### 1. Core Setup
- ✅ Installed `vue-i18n@9`
- ✅ Created i18n configuration in `/src/i18n/index.ts`
- ✅ Created translation files for all 3 languages in `/src/i18n/locales/`
- ✅ Integrated i18n into main.ts
- ✅ Created LanguageSwitcher component
- ✅ Added language switcher to AppLayout header

### 2. Translation Files Structure
```
src/i18n/
├── index.ts           # i18n configuration
└── locales/
    ├── en.ts          # English translations
    ├── ru.ts          # Russian translations
    └── tk.ts          # Turkmen translations
```

### 3. Translation Keys Available
All translation files include keys for:
- `common.*` - Common UI elements (buttons, actions, etc.)
- `nav.*` - Navigation menu items
- `dashboard.*` - Dashboard page
- `cargos.*` - Cargos page
- `vehicles.*` - Vehicles page
- `shipments.*` - Shipments page
- `offers.*` - Offers page
- `reviews.*` - Reviews page
- `wallet.*` - Wallet page
- `auth.*` - Authentication
- `userTypes.*` - User type labels
- `messages.*` - System messages

## How to Use Translations in Your Components

### In Template (HTML)
```vue
<template>
  <!-- Simple translation -->
  <h1>{{ $t('dashboard.title') }}</h1>
  
  <!-- Translation in attributes -->
  <el-button :placeholder="$t('common.search')">
  
  <!-- Translation with parameters -->
  <span>{{ $t('messages.minLength', { min: 5 }) }}</span>
</template>
```

### In Script (TypeScript)
```vue
<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Use in functions
function showMessage() {
  ElMessage.success(t('common.success'))
}

// Use in computed
const title = computed(() => t('dashboard.title'))
</script>
```

## How to Update Your Pages

### Example: Dashboard Page
Replace hardcoded text with translation keys:

**Before:**
```vue
<h1>Welcome back, {{ user?.username }}!</h1>
```

**After:**
```vue
<h1>{{ $t('dashboard.welcomeBack') }}, {{ user?.username }}! 👋</h1>
```

### Example: Button Text
**Before:**
```vue
<el-button>Add New Cargo</el-button>
```

**After:**
```vue
<el-button>{{ $t('cargos.addNew') }}</el-button>
```

### Example: Placeholder
**Before:**
```vue
<el-input placeholder="Search cargos..." />
```

**After:**
```vue
<el-input :placeholder="$t('cargos.searchPlaceholder')" />
```

## Language Switcher Usage

The language switcher is already added to the header. Users can:
1. Click the language button (shows current language: EN/RU/TM)
2. Select from dropdown: English 🇬🇧, Русский 🇷🇺, Türkmençe 🇹🇲
3. Language preference is saved to localStorage
4. Page automatically updates with new language

## Adding New Translations

### 1. Add to English (en.ts)
```typescript
export default {
  myNewSection: {
    title: 'My Title',
    description: 'My Description'
  }
}
```

### 2. Add to Russian (ru.ts)
```typescript
export default {
  myNewSection: {
    title: 'Мой заголовок',
    description: 'Моё описание'
  }
}
```

### 3. Add to Turkmen (tk.ts)
```typescript
export default {
  myNewSection: {
    title: 'Meniň adym',
    description: 'Meniň düşündirişim'
  }
}
```

### 4. Use in Component
```vue
<h1>{{ $t('myNewSection.title') }}</h1>
```

## Quick Reference: Common Translation Keys

### Buttons & Actions
- `$t('common.add')` - Add
- `$t('common.edit')` - Edit
- `$t('common.delete')` - Delete
- `$t('common.save')` - Save
- `$t('common.cancel')` - Cancel
- `$t('common.search')` - Search
- `$t('common.filter')` - Filter
- `$t('common.refresh')` - Refresh

### Navigation
- `$t('nav.dashboard')` - Dashboard
- `$t('nav.vehicles')` - Vehicles
- `$t('nav.cargos')` - Cargos
- `$t('nav.offers')` - Offers
- `$t('nav.shipments')` - Shipments
- `$t('nav.reviews')` - Reviews
- `$t('nav.wallet')` - Wallet

### Status Labels
- `$t('cargos.open')` - Open
- `$t('cargos.inProgress')` - In Progress
- `$t('cargos.delivered')` - Delivered
- `$t('shipments.paid')` - Paid
- `$t('shipments.pending')` - Pending
- `$t('offers.accepted')` - Accepted
- `$t('offers.rejected')` - Rejected

## Next Steps to Complete Translation

To fully translate your application, you need to update each page component:

1. **Dashboard** (`/src/pages/Dashboard/index.vue`)
2. **Cargos** (`/src/pages/Cargos/index.vue`)
3. **Vehicles** (`/src/pages/Vehicles/index.vue`)
4. **Shipments** (`/src/pages/Shipments/index.vue`)
5. **Offers** (`/src/pages/Offers/index.vue`)
6. **Reviews** (`/src/pages/Reviews/index.vue`)
7. **Wallet** (`/src/pages/Wallet/index.vue`)

For each page:
1. Replace all hardcoded text with `$t('key')`
2. Replace all hardcoded placeholders with `:placeholder="$t('key')"`
3. Replace all hardcoded button text with `{{ $t('key') }}`
4. Replace all hardcoded messages with `t('key')` in script section

## Testing

1. Start your development server:
   ```bash
   npm run dev
   ```

2. Open the application in your browser

3. Click the language switcher in the header

4. Switch between English, Russian, and Turkmen

5. Verify all text updates correctly

## Tips

- Always use translation keys instead of hardcoded text
- Keep translation keys organized by section
- Use descriptive key names
- Test all 3 languages after making changes
- The language preference persists across sessions (stored in localStorage)

## Support

If you need to add more translations or modify existing ones, simply edit the files in `/src/i18n/locales/` and the changes will be reflected immediately in development mode.
