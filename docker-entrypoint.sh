#!/bin/sh
                                  
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || exit 1

echo "Creating database migrations..."
python manage.py makemigrations --noinput || exit 1

echo "Applying database migrations..."
python manage.py migrate --noinput || exit 1

echo "Creating superuser..."
python manage.py createsuperuser --noinput

python manage.py runserver 0.0.0.0:8000
