#!/usr/bin/env bash
# Render build script for CareerNest backend
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Seed data only on first deploy (skip if data exists)
python manage.py seed_data 2>/dev/null || echo "Seed data already exists or skipped."
