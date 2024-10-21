# serving/app.py

from flask import Flask, request, jsonify
import mlflow
import pandas as pd
import threading
import time
import os

app = Flask(__name__)

model = None
model_version = None

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow-server:5000")
MODEL_NAME = "RandomForest_Iris"
MODEL_UPDATE_INTERVAL = 60  # in seconds

def load_latest_model():
    global model, model_version
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = mlflow.tracking.MlflowClient()

    try:
        experiment = client.get_experiment_by_name(MODEL_NAME)
        if experiment is None:
            print(f"No experiment named '{MODEL_NAME}' found.")
            return

        runs = client.search_runs(
            experiment_ids=experiment.experiment_id,
            order_by=["attributes.start_time DESC"],
            max_results=1,
            filter_string="attributes.status = 'FINISHED'"
        )

        if not runs:
            print("No completed runs found for the experiment.")
            return

        latest_run = runs[0]
        run_id = latest_run.info.run_id
        new_model_version = latest_run.info.end_time  # Using end_time as a proxy for version
        if model_version != new_model_version:
            model_uri = f"runs:/{run_id}/model"
            print(f"Loading model from {model_uri}")
            model = mlflow.sklearn.load_model(model_uri)
            model_version = new_model_version
            print(f"Loaded new model version: {model_version}")
        else:
            print("Model is up-to-date.")
    except Exception as e:
        print(f"Error loading model: {e}")

def model_update_daemon():
    while True:
        try:
            load_latest_model()
        except Exception as e:
            print(f"Error in model update daemon: {e}")
        time.sleep(MODEL_UPDATE_INTERVAL)

@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    try:
        data = request.get_json(force=True)
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Start the model update daemon thread
    threading.Thread(target=model_update_daemon, daemon=True).start()
    app.run(host='0.0.0.0', port=5001)
