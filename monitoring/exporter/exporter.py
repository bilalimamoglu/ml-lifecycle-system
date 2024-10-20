# monitoring/exporter/exporter.py

from prometheus_client import start_http_server, Gauge
import time
import mlflow
import os

def collect_metrics():
    # Define Prometheus Gauges for each metric
    model_accuracy = Gauge('model_accuracy', 'Accuracy of the ML model during evaluation')
    training_accuracy = Gauge('training_accuracy_score', 'Accuracy of the ML model during training')
    model_last_updated = Gauge('model_last_updated', 'Timestamp of the last model update in Unix time')

    # Set the MLflow tracking URI
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))

    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    print("Prometheus exporter started on port 8000")

    while True:
        try:
            client = mlflow.tracking.MlflowClient()
            experiment_name = 'RandomForest_Iris'
            experiment = client.get_experiment_by_name(experiment_name)

            if experiment:
                runs = client.search_runs(
                    experiment_ids=experiment.experiment_id,
                    order_by=["attributes.start_time DESC"],
                    max_results=1
                )

                if runs:
                    latest_run = runs[0]
                    metrics = latest_run.data.metrics
                    accuracy = metrics.get('accuracy', 0)
                    training_accuracy_score = metrics.get('training_accuracy_score', 0)

                    model_accuracy.set(accuracy)
                    training_accuracy.set(training_accuracy_score)

                    # Get the end time of the run in seconds since epoch
                    last_updated = latest_run.info.end_time / 1000
                    model_last_updated.set(last_updated)

                    print(f"Updated metrics: accuracy={accuracy}, training_accuracy_score={training_accuracy_score}")
                else:
                    print("No runs found for the experiment.")
            else:
                print(f"No experiment named '{experiment_name}' found.")
        except Exception as e:
            print(f"Error collecting metrics: {e}")

        # Wait for 60 seconds before the next update
        time.sleep(60)

if __name__ == '__main__':
    collect_metrics()
