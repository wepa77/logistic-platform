#!/usr/bin/env bash
set -euo pipefail

# This script applies migrations and seeds demo data for all models in the dasha app.
# It uses the existing Django management command `seed_ten` to create 10 records per model.
# Usage: bash seed_all.sh

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

echo "==> Applying migrations"
python manage.py migrate --noinput

echo "==> Seeding dictionaries (3 languages)"
python manage.py seed_dicts

echo "==> Seeding demo data (10 records per model)"
python manage.py seed_ten

echo "==> Done. You can now run the backend and frontend to see data in lists."
echo "Backend: python manage.py runserver"
echo "Frontend: (in django-logi-frontend) npm run dev"
