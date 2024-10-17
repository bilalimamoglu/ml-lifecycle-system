from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import os

default_args = {
    'owner': 'data_scientist',
    'depends_on_past': False,
    'email': ['your_email@example.com'],  # Replace with your email
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'sla': timedelta(hours=1),
}

with DAG(
    'daily_model_training',
    default_args=default_args,
    description='Train and log ML model daily using Docker',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    train_model = DockerOperator(
        task_id='train_model',
        image='ml-lifecycle-training:latest',  # Ensure this matches your training image
        api_version='auto',
        auto_remove=True,
        command="python model_training.py",
        docker_url="unix://var/run/docker.sock",  # Default Docker URL
        network="ml-lifecycle_system_default",  # Specify the docker-compose network
        environment={
            'MLFLOW_TRACKING_URI': 'http://mlflow-server:5000',
            'AWS_ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID'),
            'AWS_SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY'),
        },
    )
