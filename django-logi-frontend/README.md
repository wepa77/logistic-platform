# Logistics Marketplace Frontend (Vue 3 + TS + Vite)

This repository contains a Vue 3 + TypeScript frontend for a logistics marketplace (similar to ati.su) with:
- Public Marketplace landing with route search and distance calculator
- Authenticated dashboard and feature pages (Vehicles, Cargos, Offers, Shipments, Reviews, Wallet)
- Pinia store, Vue Router, Element Plus UI, Axios API client

## Quick Start
- Node 18+
- Install deps: `npm install`
- Dev server: `npm run dev`
- Type check + build: `npm run build`
- Preview built app: `npm run preview`

Set `VITE_API_URL` in your `.env` (defaults to `http://127.0.0.1:8000/api`). An interceptor injects `Authorization: Bearer <access>` from `localStorage` key `access`.

## Routes
- `/home` — Public Home page (intro + CTAs to Marketplace, Login, Register).
- `/market` — Public marketplace landing (no auth). Search for From/To/Date/Radius and quick links. A simple distance calculator is provided using OpenStreetMap Nominatim + Haversine.
- `/login`, `/register` — Public auth routes.
- `/` — Authenticated app layout (requires login):
  - `/vehicles` — Fleet management page (add/edit/remove vehicles).
  - `/cargos` — Add cargo/vehicle form page (see file comment; can be adapted to your backend payloads).
  - `/offers`, `/shipments`, `/reviews`, `/wallet` — Feature pages (connect to backend as needed).

The router guard allows public access to `/market`, `/login`, and `/register`. Unauthenticated users navigating elsewhere are redirected to `/market`.

## Marketplace Page
`src/pages/Marketplace/index.vue` is a self-contained, well-documented page that:
- Accepts user input for origin, destination, radius, and date
- Navigates to the Vehicles or Cargos pages with these values in the query string
- Calculates straight-line distance between origin and destination (demo only)

Replace the demo geocoder with your backend if needed.

## Notes
- Auto-imports for common Vue/Element Plus APIs are enabled via Vite plugins.
- i18n is available (EN/RU); when adding UI strings, update both language files.
- For deployment/CI, ensure `npm run build` succeeds and serve the resulting `dist/`.
