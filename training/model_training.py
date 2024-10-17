import os
import boto3
import logging

# Retrieve and log AWS credentials
session = boto3.Session()
credentials = session.get_credentials()

# Print out the AWS credentials to ensure they are correct
current_credentials = credentials.get_frozen_credentials()
print(f"AWS_ACCESS_KEY_ID={current_credentials.access_key}")
print(f"AWS_SECRET_ACCESS_KEY={current_credentials.secret_key}")


import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

print("S3 Buckets:")
for bucket in response['Buckets']:
    print(f"  {bucket['Name']}")

# ==========================
# 2. Import Mlflow and Other Libraries
# ==========================

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from mlflow.models import infer_signature
from pathlib import Path
from datetime import datetime
import random

# ==========================
# 3. Configure Mlflow
# ==========================

# Set Mlflow Tracking URI from environment variable
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000"))

# Define the experiment
mlflow.set_experiment("RandomForest_Iris")

# ==========================
# 4. Define Training Function
# ==========================

def train_random_forest(df: pd.DataFrame, target_column: str, hyperparameters: dict):
    """
    Train a Random Forest Classifier on the given dataset.
    """
    X = df.drop(target_column, axis=1)  # Features
    y = df[target_column]  # Target

    # Split the dataset into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Create and train the Random Forest model
    model = RandomForestClassifier(**hyperparameters)
    model.fit(X_train, y_train)

    # Predict and calculate accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, accuracy, X_test

# ==========================
# 5. Main Execution
# ==========================

if __name__ == '__main__':
    # Load Iris dataset from /data folder
    data_path = Path.cwd() / 'data' / 'iris.csv'
    df = pd.read_csv(data_path)

    # Set hyperparameters
    hyperparameters = {
        'n_estimators': random.randint(10, 100),
        'max_depth': random.randint(5, 30),
        'min_samples_split': random.randint(2, 10),
        'min_samples_leaf': random.randint(1, 4),
        'random_state': 42,
    }

    # Start an Mlflow run
    with mlflow.start_run():
        model, accuracy, X_test = train_random_forest(df, 'variety', hyperparameters)
        print("The accuracy of the model is:", accuracy)

        # Log parameters and metrics
        mlflow.log_params(hyperparameters)
        mlflow.log_metric("accuracy", accuracy)

        # Generate a signature and input example
        input_example = X_test[:1]  # Take the first row as an input example
        signature = infer_signature(X_test, model.predict(X_test))

        # Log the model with signature and input example
        mlflow.sklearn.log_model(model, "random_forest_model", signature=signature, input_example=input_example)

        # Optionally, tag the run with timestamp or version
        mlflow.set_tag("version", datetime.now().strftime("%Y%m%d%H%M%S"))
