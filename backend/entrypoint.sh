#!/usr/bin/env bash

python manage.py migrate --noinput

python manage.py collectstatic --noinput
python manage.py flush_cache
echo "Starting web service ..."
gunicorn --workers=2 --threads=4 --bind=0.0.0.0:8080 service.wsgi:application -t 300
