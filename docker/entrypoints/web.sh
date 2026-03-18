#!/bin/sh
set -e

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.prod" ]; then
    echo "Starting Gunicorn..."
    gunicorn config.wsgi:application -c docker/prod/gunicorn.conf.py
else
    echo "Starting Django development server..."
    python manage.py runserver 0.0.0.0:8000
fi
