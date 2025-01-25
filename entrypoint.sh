#!/bin/bash

# Check if required environment variables are set
: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"
: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${POSTGRES_HOST:?POSTGRES_HOST is required}"
: "${POSTGRES_PORT:?POSTGRES_PORT is required}"
: "${DJANGO_SUPERUSER_USERNAME:?DJANGO_SUPERUSER_USERNAME is required}"
: "${DJANGO_SUPERUSER_PASSWORD:?DJANGO_SUPERUSER_PASSWORD is required}"
: "${DJANGO_SUPERUSER_EMAIL:?DJANGO_SUPERUSER_EMAIL is required}"

# Wait for PostgreSQL to be available
until pg_isready -h db -p 5432; do
  echo "Waiting for database..."
  sleep 2
done

# Set password for root user
export PGPASSWORD='secret'

# Create the root role if it doesn't exist
echo "Creating root role if it doesn't exist..."
psql -h db -U root -d postgres -tc "SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_USER'" | grep -q 1 || \
  psql -h db -U root -d postgres -c "CREATE ROLE root WITH LOGIN SUPERUSER CREATEDB CREATEROLE INHERIT NOREPLICATION CONNECTION LIMIT -1 ENCRYPTED PASSWORD '$POSTGRES_PASSWORD';"

# Delete existing database if it exists
psql -h db -U root -d postgres -c "DROP DATABASE $POSTGRES_DB;"

# Create the database if it doesn't exist
echo "Creating database if it doesn't exist..."
psql -h db -U root -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || \
  psql -h db -U root -d postgres -c "CREATE DATABASE $POSTGRES_DB;"

# Make migrations if needed
echo "Making migrations..."
python manage.py makemigrations

# Run Django migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if it doesn't exist..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    print("Creating superuser...")
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
else:
    print("Superuser already exists.")
EOF

# Run the application (or your desired command)
exec "$@"
