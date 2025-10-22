import { render, fireEvent, screen, waitFor } from '@testing-library/vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import i18n from '@/i18n'
import AddVehicle from '@/pages/Vehicles/Add.vue'
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
      { path: '/vehicles/add', name: 'vehicle-add', component: { template: '<div />' } },
    ]
  })
}

async function renderPage() {
  const router = makeRouter()
  router.push('/vehicles/add')
  await router.isReady()
  return render(AddVehicle, { global: { plugins: [router, i18n] } })
}

describe('Vehicles/Add.vue insert flow', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('shows validation error when required fields are missing', async () => {
    await renderPage()

    const publishBtn = screen.getByRole('button', { name: /publish vehicle/i })
    await fireEvent.click(publishBtn)

    expect(ElMessage.error).toHaveBeenCalled()
  })

  it('submits successfully when minimal required fields are filled', async () => {
    await renderPage()

    // Minimal required: location_from per component validation (body_type optional for demo)
    const fromInput = screen.getByPlaceholderText(/from \(locality\)/i)
    await fireEvent.update(fromInput, 'Ashgabat')

    const publishBtn = screen.getByRole('button', { name: /publish vehicle/i })
    await fireEvent.click(publishBtn)

    await waitFor(() => {
      expect(fromInput).toHaveValue('')
    })
  })
})
