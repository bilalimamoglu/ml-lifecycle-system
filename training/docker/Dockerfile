# Use the official Python image
FROM python:3.11.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY ../../training/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the training script and data
COPY ../../training/model_training.py .
COPY ../../data/iris.csv ./data/iris.csv

# Set environment variables
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# Command to run the training script
CMD ["python", "model_training.py"]
