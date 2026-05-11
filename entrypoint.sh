#!/bin/bash
set -e

# Применяем миграции
python manage.py migrate --noinput

# Загружаем начальные данные, если они есть
if [ -f initial_data.json ]; then
    python manage.py loaddata initial_data.json
fi

# Собираем статику
python manage.py collectstatic --noinput

# Запускаем Gunicorn
exec gunicorn foodtruck_site.wsgi:application --bind 0.0.0.0:8000
