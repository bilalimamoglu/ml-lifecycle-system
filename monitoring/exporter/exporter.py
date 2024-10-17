from prometheus_client import start_http_server, Gauge
import time
import mlflow
from mlflow.tracking import MlflowClient
import os
import requests

# Define the port where Prometheus will scrape metrics
PROMETHEUS_PORT = 8000

# Define Prometheus metrics
accuracy_gauge = Gauge('mlflow_model_accuracy', 'Accuracy of the ML model')
model_timestamp_gauge = Gauge('model_training_timestamp', 'Timestamp of the latest model training')

# Initialize Mlflow client
mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', "http://mlflow-server:5000"))
client = MlflowClient()

def fetch_latest_metrics():
    experiments = client.list_experiments()
    latest_run = None
    latest_start_time = 0

    for experiment in experiments:
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["attributes.start_time DESC"],
            max_results=1
        )
        if runs and runs[0].info.start_time > latest_start_time:
            latest_start_time = runs[0].info.start_time
            latest_run = runs[0]

    if latest_run:
        accuracy = latest_run.data.metrics.get("accuracy", 0)
        accuracy_gauge.set(accuracy)
        model_timestamp_gauge.set(latest_run.info.start_time / 1000)  # Convert ms to seconds

if __name__ == '__main__':
    # Start Prometheus metrics server
    start_http_server(PROMETHEUS_PORT)
    print(f"Prometheus exporter started on port {PROMETHEUS_PORT}")

    # Periodically fetch and update metrics
    while True:
        fetch_latest_metrics()
        time.sleep(60)  # Fetch every 60 seconds
