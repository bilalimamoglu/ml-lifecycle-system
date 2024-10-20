# Use the specified Airflow base image
FROM apache/airflow:2.10.2-python3.11

# Switch to root to install system dependencies
USER root

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Copy the entrypoint script to the correct location
COPY entrypoint.sh /entrypoint.sh

# Set permissions
RUN chmod +x /entrypoint.sh

# Switch back to airflow user
USER airflow

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add the python_scripts directory to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/python_scripts"

# Copy DAGs and scripts to appropriate locations
COPY dags/python_scripts/ /opt/airflow/python_scripts/
COPY dags/ /opt/airflow/dags/

# Create data directory
RUN mkdir -p /opt/airflow/data

# Expose port 8080
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
