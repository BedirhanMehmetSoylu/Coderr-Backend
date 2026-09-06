#!/usr/bin/env bash
# Executed by Render before each deploy
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create a superuser automatically on first deploy (Render's free tier has
# no shell access, so this is the only way to get an admin account).
# Safe to run on every deploy: does nothing if the user already exists or
# if the env vars are not set.
python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser \"{username}\" created.')
    else:
        print(f'Superuser \"{username}\" already exists, skipping.')
else:
    print('DJANGO_SUPERUSER_USERNAME/PASSWORD not set, skipping superuser creation.')
"
