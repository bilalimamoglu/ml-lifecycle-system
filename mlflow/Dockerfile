# Use the official lightweight Python image
FROM python:3.11.9-slim

# Install Mlflow and AWS CLI
RUN pip install mlflow boto3 psycopg2-binary

# Set environment variables for Mlflow and AWS
ENV MLFLOW_S3_ENDPOINT_URL=https://s3.amazonaws.com
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Expose the default port for Mlflow
EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0"]
