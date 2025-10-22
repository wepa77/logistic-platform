import { render, fireEvent, screen } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import i18n from '@/i18n'
import AddCargo from '@/pages/Cargos/Add.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'

// Partially mock Element Plus just for ElMessage, keep other exports intact
vi.mock('element-plus', async () => {
  const actual = await vi.importActual<any>('element-plus')
  return {
    ...actual,
    ElMessage: {
      success: vi.fn(),
      error: vi.fn(),
      warning: vi.fn(),
      info: vi.fn()
    }
  }
})

import { ElMessage } from 'element-plus'

function makeRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/cargos/add', name: 'cargo-add', component: { template: '<div />' } },
    ]
  })
}

async function renderPage() {
  const router = makeRouter()
  router.push('/cargos/add')
  await router.isReady()
  return render(AddCargo, { global: { plugins: [router, i18n] } })
}

describe('Cargos/Add.vue insert flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows validation error when required fields are missing', async () => {
    await renderPage()

    const publishBtn = screen.getByRole('button', { name: /publish cargo/i })
    await fireEvent.click(publishBtn)

    expect(ElMessage.error).toHaveBeenCalled()
  })

  it('submits successfully when minimal required fields are filled', async () => {
    await renderPage()

    // Fill minimal required fields used by inline validation
    const cargoName = screen.getByPlaceholderText(/cargo name/i)
    await fireEvent.update(cargoName, 'Test Cargo')

    const pickupAddress = screen.getByPlaceholderText(/pickup address/i)
    await fireEvent.update(pickupAddress, 'Ashgabat')

    const deliveryAddress = screen.getByPlaceholderText(/delivery address/i)
    await fireEvent.update(deliveryAddress, 'Mary')

    // Date picker is Element Plus; we can set its input by role placeholder too
    const pickupDate = screen.getByPlaceholderText(/pickup date/i)
    await fireEvent.update(pickupDate, '2025-10-22')

    const publishBtn = screen.getByRole('button', { name: /publish cargo/i })
    await fireEvent.click(publishBtn)

    expect(ElMessage.success).toHaveBeenCalled()
  })
})
