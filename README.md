# logistic-platform

## Quick seed script (includes 3-language dictionaries)

Run this script to apply migrations, seed all dictionaries (tk/ru/en), and create demo data so you can see lists in the frontend:

bash seed_all.sh

It will first populate all dictionary tables with localized values, then create 10 records for each main model in the `dasha` app:
- Users: 10 (5 carriers with sufficient deposit, 5 shippers)
- Vehicles: 10
- Cargos: 10
- Offers: 10
- Shipments: 10 (one per cargo)
- Reviews: 10 (one per shipment)
- Wallet Transactions: 10
- TopUp Requests: 10

## Manual seeding (alternative)

If you prefer manual commands:

1. Apply migrations:

   python manage.py migrate

2. Create demo data:

   python manage.py seed_ten

You can run the seed command multiple times; it will create new uniquely-named records on each run without altering existing data.

## View in frontend

1. Start Django API:

   python manage.py runserver

2. Start the frontend dev server:

   cd django-logi-frontend
   npm install
   npm run dev

3. Open the app in the browser and navigate to lists:
- /vehicles
- /cargos
- /offers
- /shipments
- /reviews
- /wallet

## New search pages

Public search pages are available in the frontend (no authentication required):

- /search/cargos — Search cargoes
- /search/vehicles — Search vehicles

Personal sections in the top navigation were renamed for clarity:
- Vehicles → My vehicles (/vehicles)
- Cargos → My cargos (/cargos)


## Models Overview

This project uses Django models under the dasha app to power a logistics marketplace.
Below is a brief description of each model and its relationships.

- User (extends AbstractUser)
  - Purpose: Platform account with role (user_type) and profile fields.
  - Key fields: user_type, phone, company_name, address, verified, balance, deposit_balance, avatar.
  - Relations: owns Vehicles; can create Cargos (as shipper), make Offers (as carrier), execute Shipments, post Reviews, has WalletTransactions and TopUpRequests.

- Vehicle
  - Purpose: A carrier’s vehicle available for transporting cargo.
  - Key fields: body_type, load_type, truck_category, capacity_kg, volume_m3, length/width/height, features (ADR/TIR/GPS/Lift/Horses), availability and locations, rate fields, company/contact info, promo flags.
  - Relations: owner → User (carrier). May be referenced by Offers and Shipments.

- Cargo
  - Purpose: A cargo posting created by a shipper, specifying what, when, and how to transport.
  - Key fields: title, description, weight_kg, volume_m3, quantity, packing_type; ready_status, pickup/delivery dates and times, addresses, customs flag, route_info; body/load/unload types, FTL/LTL flags and equipment; rate and currency; payment terms; company/contact; promo flags; status.
  - Relations: shipper → User. May have many Offers. Optionally linked one-to-one to a Shipment when executed.

- Offer
  - Purpose: A carrier’s proposal to move a specific Cargo.
  - Key fields: price, note, status, created_at.
  - Relations: cargo → Cargo, carrier → User, vehicle → Vehicle (optional).

- Shipment
  - Purpose: Execution record of a Cargo being transported.
  - Key fields: start/end time, total_price, distance_km, payment_type, payment_status, cash_received_by, received_date, commission_amount.
  - Relations: cargo → Cargo (one-to-one), carrier → User, vehicle → Vehicle (optional).

- Review
  - Purpose: Feedback after a Shipment is completed.
  - Key fields: rating (1-5), comment, created_at.
  - Relations: shipment → Shipment (one-to-one), reviewer → User.

- WalletTransaction
  - Purpose: Ledger entries for user balance and deposit changes.
  - Key fields: tx_type, amount, description, created_at, success.
  - Relations: user → User.

- TopUpRequest
  - Purpose: Requests to increase user balance (manual/offline supported; may store provider session id).
  - Key fields: amount, stripe_session_id, created_at, paid.
  - Relations: user → User.

### Dictionary models (localizable, read-only in API)
All dictionary models inherit from DictionaryBase with fields: code, name_tk, name_ru, name_en, is_active, ordering, timestamps.
They are used to populate select lists in the UI and keep options manageable and localized.

- UserTypeDict — user roles for accounts.
- ShipmentPaymentTypeDict — payment methods for shipments.
- ShipmentPaymentStatusDict — payment statuses for shipments.
- WalletTransactionTypeDict — categories of wallet operations.
- VehicleBodyTypeDict — vehicle body types.
- VehicleLoadTypeDict — vehicle load/unload methods.
- VehicleTruckCategoryDict — vehicle categories (semi-trailer, truck, coupling).
- VehicleRateTypeDict — rate modes for vehicles.
- CurrencyDict — supported currencies.
- CargoBodyTypeDict — required body types for cargo.
- CargoLoadTypeDict — cargo load/unload methods.
- CargoRateTypeDict — rate modes for cargo.
- CargoPaymentMethodDict — payment methods for cargo.
- CompanyTypeDict — legal entity types.
- CargoStatusDict — cargo lifecycle statuses.
- CargoTypeDict — cargo kinds (general, fragile, hazardous, etc.).
- ReadyStatusDict — cargo readiness (ready, in_3_days, in_7_days).
- VehicleTruckTypeDict — truck types (box, flatbed, refrigerated, tanker, other).

Notes
- Dictionary endpoints are exposed at /dicts/* via DRF viewsets; only active entries (is_active=True) are listed, ordered by the ordering field.
- Core entity endpoints (users, vehicles, cargos, offers, shipments, reviews, wallet, topups) are available via the DRF router.
