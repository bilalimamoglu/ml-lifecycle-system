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

    # Load the latest model
    current_run = mlflow.active_run()
    if current_run is None:
        print("No active MLflow run found. Cannot load model.")
        return

    model_uri = f"runs:/{current_run.info.run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)

    # Evaluate model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric('accuracy', accuracy)
    print(f"Model evaluation completed with accuracy: {accuracy}")
