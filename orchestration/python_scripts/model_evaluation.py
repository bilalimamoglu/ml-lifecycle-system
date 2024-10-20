# orchestration/scripts/model_evaluation.py
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import mlflow
import mlflow.sklearn

def evaluate_model():
    data_dir = Path('/opt/orchestration/data')
    X_test = pd.read_csv(data_dir / 'X_test.csv')
    y_test = pd.read_csv(data_dir / 'y_test.csv').values.ravel()

    # Standardize features
    scaler = StandardScaler()
    X_test_scaled = scaler.fit_transform(X_test)

    # Configure MLflow
    mlflow.set_tracking_uri('http://mlflow-server:5000')

    # Load the latest model
    model_uri = 'runs:/{}/model'.format(mlflow.active_run().info.run_id)
    model = mlflow.sklearn.load_model(model_uri)

    # Evaluate model
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric('accuracy', accuracy)
    print(f"Model evaluation completed with accuracy: {accuracy}")
