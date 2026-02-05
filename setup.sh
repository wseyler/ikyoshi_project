#!/usr/bin/env bash
# One-time setup so this Django project runs on this machine.
# Run from project root: ./setup.sh   or   bash setup.sh

set -e
cd "$(dirname "$0")"
PROJECT_ROOT="$PWD"

echo "==> Project root: $PROJECT_ROOT"

# Prefer ARM Homebrew Python when available
if [ -x /opt/homebrew/bin/python3 ]; then
  PYTHON=/opt/homebrew/bin/python3
  echo "==> Using ARM Homebrew Python: $PYTHON"
else
  PYTHON=$(command -v python3)
  echo "==> Using: $PYTHON"
fi

echo "==> Removing old venv (if any)..."
rm -rf venv

echo "==> Creating virtual environment..."
"$PYTHON" -m venv venv

echo "==> Upgrading pip..."
./venv/bin/pip install --upgrade pip --quiet

echo "==> Installing dependencies (SQLite-only, no mysqlclient)..."
./venv/bin/pip install -r requirements-local.txt --quiet

echo "==> Running migrations..."
./venv/bin/python manage.py migrate

echo ""
echo "Setup complete. To run the app:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo "  Then open http://127.0.0.1:8000/"
echo ""
