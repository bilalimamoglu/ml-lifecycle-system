import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import random
import boto3
import datetime
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def train_model():
    # Configure Boto3 for AWS S3 Access
    try:
        print(f"AWS_SHARED_CREDENTIALS_FILE: {os.getenv('AWS_SHARED_CREDENTIALS_FILE')}")
        print(f"AWS_CONFIG_FILE: {os.getenv('AWS_CONFIG_FILE')}")
        session = boto3.Session()
        credentials = session.get_credentials()
        current_credentials = credentials.get_frozen_credentials()
        print(f"AWS_ACCESS_KEY_ID={current_credentials.access_key}")
        print(f"AWS_SECRET_ACCESS_KEY={current_credentials.secret_key}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials not found:", e)
        return

    data_dir = Path('/opt/airflow/data')
    X_train = pd.read_csv(data_dir / 'X_train.csv')
    y_train = pd.read_csv(data_dir / 'y_train.csv').values.ravel()

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Hyperparameters
    hyperparameters = {
        'n_estimators': random.randint(10, 100),
        'max_depth': random.randint(5, 30),
        'min_samples_split': random.randint(2, 10),
        'min_samples_leaf': random.randint(1, 4),
        'random_state': 42,
    }

    # Generate a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Configure MLflow
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))
    mlflow.set_experiment('RandomForest_Iris')

    with mlflow.start_run():
        # Train model
        model = RandomForestClassifier(**hyperparameters)
        model.fit(X_train_scaled, y_train)

        # Log parameters and model
        mlflow.log_params(hyperparameters)
        signature = infer_signature(X_train_scaled, model.predict(X_train_scaled))
        artifact_path = "model"
        mlflow.sklearn.log_model(model, artifact_path, signature=signature)
        print(f"Model training completed and logged to MLflow with artifact path: {artifact_path}")
