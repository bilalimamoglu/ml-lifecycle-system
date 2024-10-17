#!/bin/bash
# Initialize Airflow and create a default admin user
airflow db migrate
airflow users create \
    --username myuser \
    --password mypassword \
    --firstname Firstname \
    --lastname Lastname \
    --role Admin \
    --email example@example.com

# Start Airflow webserver and scheduler
airflow webserver --port 8080 &
airflow scheduler
