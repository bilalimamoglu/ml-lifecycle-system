# evaluate_model.py

import os
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import mlflow
import mlflow.sklearn
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def evaluate_model():
    # Configure Boto3 for AWS S3 Access
    try:
        session = boto3.Session()
        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()
        print(f"AWS_ACCESS_KEY_ID={current_credentials.access_key}")
        print(f"AWS_SECRET_ACCESS_KEY={current_credentials.secret_key}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials not found:", e)
        return

    data_dir = Path('/opt/airflow/data')
    X_test = pd.read_csv(data_dir / 'X_test.csv')
    y_test = pd.read_csv(data_dir / 'y_test.csv').values.ravel()

    # Standardize features
    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    # Configure MLflow
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))
    client = mlflow.tracking.MlflowClient()

    # Find the latest run
    experiment_name = 'RandomForest_Iris'
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"No experiment named '{experiment_name}' found.")
        return

    runs = client.search_runs(experiment_ids=experiment.experiment_id,
                              order_by=["attributes.start_time DESC"],
                              max_results=1)

    if not runs:
        print("No runs found for the experiment.")
        return

    latest_run = runs[0]
    run_id = latest_run.info.run_id

    # Use the fixed artifact path
    model_uri = f"runs:/{run_id}/model"

    # Load the model
    model = mlflow.sklearn.load_model(model_uri)

    # Evaluate model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model evaluation completed with accuracy: {accuracy}")

    # Log the accuracy metric to the latest run
    with mlflow.start_run(run_id=run_id, nested=True):
        mlflow.log_metric('accuracy', accuracy)
        print(f"Logged 'accuracy' metric to run_id: {run_id}")
