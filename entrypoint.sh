#!/bin/bash
set -e

# Применяем миграции
python manage.py migrate --noinput

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем Gunicorn
exec gunicorn foodtruck_site.wsgi:application --bind 0.0.0.0:8000
