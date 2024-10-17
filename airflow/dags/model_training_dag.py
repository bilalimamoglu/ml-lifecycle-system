from airflow import DAG
from airflow.operators.bash import BashOperator
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
    description='Train and log ML model daily',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    train_model = BashOperator(
        task_id='train_model',
        bash_command='source ~/Projects/ml-lifecycle-system/myenv/bin/activate && python ~/Projects/ml-lifecycle-system/training/model_training.py',
        env={
            'MLFLOW_TRACKING_URI': 'http://mlflow-server:5000',
        },
    )
