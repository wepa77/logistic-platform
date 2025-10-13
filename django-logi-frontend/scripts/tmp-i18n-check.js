#!/usr/bin/env node
// Temporary i18n key parity checker for en/ru/tk
// Usage: node scripts/tmp-i18n-check.js
const fs = require('fs')
const path = require('path')
const vm = require('vm')

const localesDir = path.resolve(__dirname, '../src/i18n/locales')
const files = ['en.ts', 'ru.ts', 'tk.ts']

function loadLocale(file) {
  const full = path.join(localesDir, file)
  const src = fs.readFileSync(full, 'utf8')
  // naive transform: turn `export default { ... }` into `(module.exports = { ... })`
  const transformed = src
    .replace(/export\s+default\s+{/, 'module.exports = {')
    .replace(/}\s*;?\s*$/, '}')
  const sandbox = { module: { exports: {} }, exports: {} }
  vm.createContext(sandbox)
  vm.runInContext(transformed, sandbox, { filename: file })
  return sandbox.module.exports
}

function flatten(obj, prefix = '') {
  const out = {}
  for (const [k, v] of Object.entries(obj || {})) {
    const key = prefix ? `${prefix}.${k}` : k
    if (v && typeof v === 'object' && !Array.isArray(v)) Object.assign(out, flatten(v, key))
    else out[key] = true
  }
  return out
}

let failed = false
const loaded = {}
for (const f of files) loaded[f.replace('.ts','')] = loadLocale(f)

const base = flatten(loaded.en)
for (const [name, obj] of Object.entries(loaded)) {
  const flat = flatten(obj)
  const missing = Object.keys(base).filter(k => !(k in flat))
  const extra = Object.keys(flat).filter(k => !(k in base))
  if (missing.length) {
    console.error(`Locale ${name} is missing ${missing.length} keys:`)
    missing.slice(0, 20).forEach(k => console.error('  -', k))
    if (missing.length > 20) console.error(`  ... and ${missing.length - 20} more`)
    failed = true
  }
  if (extra.length) {
    console.error(`Locale ${name} has ${extra.length} extra keys not in en:`)
    extra.slice(0, 20).forEach(k => console.error('  +', k))
    if (extra.length > 20) console.error(`  ... and ${extra.length - 20} more`)
    // not failing build on extra; uncomment to enforce strict parity
    // failed = true
  }
}

if (!failed) {
  console.log('i18n parity OK: en/ru/tk have matching keys')
  process.exit(0)
} else {
  process.exit(1)
}
