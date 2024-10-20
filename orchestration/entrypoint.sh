#!/bin/bash
set -e

# Initialize the Airflow database
airflow db upgrade

# Create an admin user if it doesn't already exist
airflow users create \
    --username myuser \
    --password mypassword \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email example@example.com \
    || echo "Admin user already exists."

# Start the Airflow webserver and scheduler
exec airflow webserver & airflow scheduler
