FROM python:3.11.9-slim

# Install dependencies
RUN pip install --no-cache-dir mlflow boto3

# Set environment variables
ENV MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
ENV MLFLOW_BACKEND_STORE_URI=sqlite:///mlflow.db
ENV MLFLOW_DEFAULT_ARTIFACT_ROOT=s3://mlflow-artifacts-bilalimg/

# Expose port
EXPOSE 5000

# Start Mlflow server
CMD ["mlflow", "server",
     "--backend-store-uri", "sqlite:///mlflow.db",
     "--default-artifact-root", "s3://mlflow-artifacts-bilalimg/",
     "--host", "0.0.0.0"]


# Add test script
COPY test_mlflow.py /test_mlflow.py

# Start Mlflow server and run test after a delay
CMD ["sh", "-c", "mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://mlflow-artifacts-bilalimg/ --host 0.0.0.0 & sleep 10 && python /test_mlflow.py && wait"]