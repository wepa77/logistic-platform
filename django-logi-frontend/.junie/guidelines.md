Project-specific development guidelines

Context
- Stack: Vite + Vue 3 + TypeScript, Pinia, Vue Router, Element Plus, Axios. No bundled unit-test framework at present.
- Aliases and auto-imports: Path alias @ → /src; unplugin-auto-import and unplugin-vue-components are configured in vite.config.ts to auto-import common Vue/Element Plus symbols and components.
- API layer: Axios instance in src/api/api.ts with baseURL from VITE_API_URL. An interceptor injects Authorization: Bearer <access> from localStorage key "access".
- i18n: Locale files in src/i18n/locales/<lang>.ts export nested objects. Keep key parity across languages.

Build and configuration
- Node and package manager: Use Node 18+ (LTS recommended). NPM is used in this repo.
- Install: npm ci (CI) or npm install (local).
- Dev server: npm run dev (Vite). Default port is shown by Vite; hot module reload is enabled.
- Type check + production build: npm run build runs vue-tsc -b then vite build to emit dist/.
- Preview built app: npm run preview serves dist/ locally.
- Environment variables:
  - VITE_API_URL: Backend API base (defaults to http://127.0.0.1:8000/api). Vite exposes only variables prefixed with VITE_. Define per-mode in .env, .env.local, .env.development, etc.
- TS/paths:
  - The @ alias maps to /src in Vite config and tsconfig paths. Prefer absolute imports from @ to reduce brittle relative paths.

Testing: how to run today and how to add proper tests
- No test framework is currently installed. Two pragmatic options:
  1) Use type checking and build as a smoke test: npm run build must pass (vue-tsc + Vite bundling).
  2) Add Vitest for unit/component testing when needed (recommended).
     - Install: npm i -D vitest @vitejs/plugin-vue jsdom @testing-library/vue @testing-library/jest-dom
     - vite.config.ts: ensure test environment is set (e.g., test: { environment: 'jsdom' }).
     - Add scripts: "test": "vitest", "test:run": "vitest run".
     - Place tests in src/**/*.test.ts[x].

Temporary example test (no new deps)
- We verified a self-contained Node script that checks i18n key parity between src/i18n/locales/en.ts and src/i18n/locales/ru.ts. This demonstrates how to create and run a simple check with the current toolchain:
  - Create scripts/tmp-i18n-check.js with a small loader that safely evaluates the locale files in a VM sandbox and compares deep keys.
  - Run: node scripts/tmp-i18n-check.js. Exit code 0 means parity holds; non-zero means keys are missing/mismatched. We ran this locally and confirmed it executes.
  - After verification, remove the temporary script to keep the repo clean.

Guidelines for adding and running tests (project-specific)
- If adopting Vitest:
  - Unit tests for pure utilities (formatters, mappers) should not touch network. Use dependency injection around API wrappers in src/api (e.g., pass axios instance) to make mocking straightforward.
  - For i18n, add a guard test that compares keys across locales (you can migrate the temporary script logic into a Vitest test).
  - For store (Pinia): use createTestingPinia or setActivePinia(new Pinia()) in tests; mock API calls via vi.mock('axios').
  - For components relying on Element Plus, prefer testing the rendered text/ARIA and emitted events rather than library internals.
- Smoke checks without a test framework:
  - Type-only smoke: npm run build must pass (vue-tsc + Vite).
  - Linting is not configured; if needed, add ESLint + Prettier, but keep settings consistent with auto-imported globals from Vite plugins.

Conventions and tips specific to this codebase
- API:
  - src/api/api.ts centralizes axios with baseURL and token injection from localStorage key "access". To avoid tight coupling in components, prefer wrapping raw calls in dedicated functions (which is already done) so they are mockable.
  - Handle FormData for file uploads (see vehicles APIs). Keep headers implicit—axios handles FormData boundary.
- Routing and pages:
  - Pages live in src/pages with index.vue per section. Navigation labels come from i18n.nav.*; avoid hard-coded English strings.
- i18n:
  - Maintain key parity across en and ru. Missing keys should default gracefully but avoid runtime gaps by validating during CI (e.g., via the parity test).
- Types:
  - Use types in src/types/models (if present) and ensure API wrappers have typed responses (see src/api/offers/index.ts). Prefer Partial<T> for patch payloads.
- Auto-imports:
  - The project uses unplugin-auto-import and unplugin-vue-components; avoid manual imports for common Vue APIs and Element Plus components unless necessary. Beware that type-aware editors still need correct tsconfig paths.

Known pitfalls
- VITE_API_URL must be set correctly for non-local backends; otherwise requests go to http://127.0.0.1:8000/api.
- Authorization header relies on the "access" token in localStorage; ensure auth flow writes/refreshes it consistently to avoid 401s.
- When migrating to a test framework, jsdom is required for component tests; Element Plus relies on DOM APIs.

Suggested CI steps (if/when added)
- npm ci
- npm run build
- Run i18n parity check (migrated to Vitest or as a node script) to catch missing translation keys.

Reproducing the temporary test locally (what we ran)
- From repo root:
  1) Create scripts/tmp-i18n-check.js (see description above).
  2) node scripts/tmp-i18n-check.js
  3) Remove the script once done to keep the repo clean.

Housekeeping
- Keep locales synchronized when adding UI strings.
- Prefer type-safe API contracts and narrow payloads.
- Add Vitest when starting to add unit tests; wire CI to run both build and tests.
