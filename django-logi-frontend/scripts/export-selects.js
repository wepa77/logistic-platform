// Simple exporter to collect cargo and vehicle select options into selects.txt
// Usage: node scripts/export-selects.js

import fs from 'node:fs'
import path from 'node:path'

import { fileURLToPath } from 'node:url'
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const root = path.resolve(__dirname, '..')

function read(file) {
  return fs.readFileSync(file, 'utf8')
}

function parseCargoTypes(addVueSource) {
  const m = addVueSource.match(/const\s+cargoTypes:[\s\S]*?=\s*\{([\s\S]*?)\}\s*/)
  if (!m) return []
  const body = m[1]
  const entries = []
  // lines like: key: 'Label',
  const re = /([a-zA-Z0-9_]+)\s*:\s*'([^']+)'/g
  let mm
  while ((mm = re.exec(body))) {
    entries.push({ value: mm[1], label: mm[2] })
  }
  return entries
}

function parseReadyStatus(addVueSource) {
  // Find the ready_status select block and collect value/label (label may be via $t, use value only)
  const block = addVueSource.match(/v-model="form\.ready_status"[\s\S]*?<\/el-select>/)
  if (!block) return []
  const options = []
  const re = /<el-option[^>]*?value="([^"]+)"/g
  let m
  while ((m = re.exec(block[0]))) options.push(m[1])
  return options
}

function parseTruckTypes(vehiclesIndexSource) {
  const block = vehiclesIndexSource.match(/label="Truck Type"[\s\S]*?<el-select[\s\S]*?>([\s\S]*?)<\/el-select>/)
  if (!block) return []
  const optionsBlock = block[1]
  const options = []
  const re = /<el-option\s+label="([^"]+)"\s+value="([^"]+)"\s*\/>/g
  let m
  while ((m = re.exec(optionsBlock))) options.push({ label: m[1], value: m[2] })
  return options
}

function extractDictEndpoints(dictsSource) {
  // Map function names to endpoints
  const re = /export\s+const\s+(get[A-Za-z0-9_]+)\s*=\s*\(\)\s*=>\s*list\('(.*?)'\)/g
  const map = {}
  let m
  while ((m = re.exec(dictsSource))) {
    map[m[1]] = m[2]
  }
  return map
}

function main() {
  const cargoAdd = read(path.join(root, 'src/pages/Cargos/Add.vue'))
  const vehiclesIndex = read(path.join(root, 'src/pages/Vehicles/index.vue'))
  const dicts = read(path.join(root, 'src/api/dicts.ts'))

  const dictMap = extractDictEndpoints(dicts)
  const cargoTypes = parseCargoTypes(cargoAdd)
  const readyStatuses = parseReadyStatus(cargoAdd)
  const truckTypes = parseTruckTypes(vehiclesIndex)

  const lines = []
  lines.push('Cargo Selects:')
  lines.push('- cargo_type (static):')
  cargoTypes.forEach(it => lines.push(`  - ${it.value}: ${it.label}`))
  lines.push(`- body_type (dictionary): ${dictMap.getCargoBodyTypes || '/dicts/cargo-body-types/'}`)
  lines.push(`- load_types (dictionary): ${dictMap.getCargoLoadTypes || '/dicts/cargo-load-types/'}`)
  lines.push(`- ready_status (static values): ${readyStatuses.join(', ') || 'ready, in_3_days, in_7_days'}`)
  lines.push(`- load_type (dictionary): ${dictMap.getCargoLoadTypes || '/dicts/cargo-load-types/'}`)
  lines.push(`- unload_type (dictionary): ${dictMap.getCargoLoadTypes || '/dicts/cargo-load-types/'}`)
  lines.push(`- rate_currency (dictionary): ${dictMap.getCurrencies || '/dicts/currencies/'}`)
  lines.push(`- payment_method (dictionary): ${dictMap.getCargoPaymentMethods || '/dicts/cargo-payment-methods/'}`)
  lines.push(`- company_type (dictionary): ${dictMap.getCompanyTypes || '/dicts/company-types/'}`)

  lines.push('')
  lines.push('Vehicle Selects:')
  lines.push(`- body_type (dictionary): ${dictMap.getVehicleBodyTypes || '/dicts/vehicle-body-types/'}`)
  lines.push(`- load_types (dictionary): ${dictMap.getVehicleLoadTypes || '/dicts/vehicle-load-types/'}`)
  lines.push(`- rate_currency (dictionary): ${dictMap.getCurrencies || '/dicts/currencies/'}`)
  lines.push(`- company_type (dictionary): ${dictMap.getCompanyTypes || '/dicts/company-types/'}`)
  lines.push('- truck_type (static):')
  truckTypes.forEach(it => lines.push(`  - ${it.value}: ${it.label}`))

  const outPath = path.join(root, 'selects.txt')
  fs.writeFileSync(outPath, lines.join('\n'), 'utf8')
  console.log(`Wrote ${outPath}`)
}

main()
