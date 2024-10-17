# Use the official lightweight Python image
FROM python:3.11.9-slim

# Install Mlflow and AWS CLI
RUN pip install --no-cache-dir mlflow boto3

# Set environment variables for Mlflow and AWS
ENV MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Expose the default port for Mlflow
EXPOSE 5000

# Start Mlflow server with the correct CMD syntax
CMD ["mlflow", "server", "--backend-store-uri=sqlite:///mlflow.db", "--default-artifact-root=s3://mlflow-artifacts-bilalimg/", "--host", "0.0.0.0"]
