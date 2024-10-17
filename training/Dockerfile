# Use the official Python image as the base
FROM python:3.11.9-slim

# Install Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the training scripts and data generation script
COPY model_training.py .
COPY generate_iris.py .
COPY run.sh .

# Make the run.sh script executable
RUN chmod +x run.sh

# Create the data directory
RUN mkdir -p /app/data

# Set environment variables
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000

# Define the default command to run the training process
CMD ["./run.sh"]
