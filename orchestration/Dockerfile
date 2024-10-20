# Use the specified Airflow base image
FROM apache/airflow:2.10.2-python3.11

# Switch to root to install system dependencies
USER root

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs and scripts
COPY dags/ /opt/airflow/dags/
COPY python_scripts/ /opt/airflow/python_scripts/

# Create data directory
RUN mkdir -p /opt/airflow/data

# Expose port 8080
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
