from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Update the import path to match the new location
from python_scripts.data_generation import generate_data
from python_scripts.data_preprocessing import preprocess_data
from python_scripts.model_training import train_model
from python_scripts.model_evaluation import evaluate_model


default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_model_training',
    default_args=default_args,
    description='ETL and ML pipeline using PythonOperator',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:

    generate_data_task = PythonOperator(
        task_id='generate_data',
        python_callable=generate_data,
    )

    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data,
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
    )

    evaluate_model_task = PythonOperator(
        task_id='evaluate_model',
        python_callable=evaluate_model,
    )

    generate_data_task >> preprocess_data_task >> train_model_task >> evaluate_model_task
