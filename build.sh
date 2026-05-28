#!/usr/bin/env bash
# Render build script for StudyStack
set -o errexit

echo "==> Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files"
python3 manage.py collectstatic --noinput

echo "==> Running database migrations"
python3 manage.py migrate --noinput

echo "==> Creating admin user (if env vars set)"
python3 manage.py initadmin || true

echo "==> Build complete"
