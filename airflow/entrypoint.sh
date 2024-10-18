#!/bin/bash
set -e

# Initialize the Airflow database
airflow db upgrade

# Create an admin user if it doesn't already exist
airflow users create \
    --username airflow \
    --password airflow \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email admin@example.com \
    || echo "Admin user already exists."

# Start the Airflow webserver in the background
airflow webserver --port 8080 &

# Start the Airflow scheduler
exec airflow scheduler
