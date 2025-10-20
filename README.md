# logistic-platform

## Quick seed script (adds records for all models)

Run this script to apply migrations and create demo data so you can see lists in the frontend:

bash seed_all.sh

It will create 10 records for each model in the `dasha` app:
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
