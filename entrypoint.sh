#!/bin/sh
set -eu

if [ "${DATABASE_ENGINE:-sqlite3}" = "mysql" ]; then
    python - <<'PY'
import os
import socket
import sys
import time

host = os.environ.get("DB_HOST", "")
port = int(os.environ.get("DB_PORT", "3306"))
if not host:
    sys.exit("DB_HOST must be set when DATABASE_ENGINE=mysql")

deadline = time.monotonic() + int(os.environ.get("DB_WAIT_TIMEOUT", "60"))
while True:
    try:
        with socket.create_connection((host, port), timeout=3):
            break
    except OSError as exc:
        if time.monotonic() >= deadline:
            sys.exit(f"Database {host}:{port} did not become ready: {exc}")
        time.sleep(2)
PY
fi

# Seed only a genuinely empty volume. Existing uploads are never overwritten.
if [ -d /app/media-seed ] && [ -z "$(find /app/media -mindepth 1 -print -quit 2>/dev/null)" ]; then
    cp -a /app/media-seed/. /app/media/
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers "${GUNICORN_WORKERS:-3}" \
    --timeout "${GUNICORN_TIMEOUT:-120}" \
    --access-logfile - \
    --error-logfile -
