#! bin/sh

python manage.py migrate

gunicorn ec.wsgi:application --bind 0.0.0.0:8000