# exporter.py
from prometheus_client import start_http_server, Gauge
import time
import mlflow

def collect_metrics():
    model_accuracy = Gauge('model_accuracy', 'Accuracy of the ML model')
    start_http_server(8000)
    while True:
        client = mlflow.tracking.MlflowClient()
        experiment_name = 'RandomForest_Iris'
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment:
            runs = client.search_runs(experiment_ids=experiment.experiment_id,
                                      order_by=["attributes.start_time DESC"],
                                      max_results=1)
            if runs:
                latest_run = runs[0]
                accuracy = latest_run.data.metrics.get('accuracy', 0)
                model_accuracy.set(accuracy)
        time.sleep(60)  # Update every 60 seconds

if __name__ == '__main__':
    collect_metrics()
