import '@testing-library/jest-dom/vitest'

// Silence ResizeObserver missing in jsdom warnings used by Element Plus
class ResizeObserverStub {
  observe() {}
  unobserve() {}
  disconnect() {}
}
// @ts-ignore
global.ResizeObserver = global.ResizeObserver || ResizeObserverStub as any
