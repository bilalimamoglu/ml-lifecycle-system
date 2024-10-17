# Use the official Airflow image as the base
FROM apache/airflow:2.10.2-python3.11

# Switch to root to install system dependencies
USER root

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Grant the 'airflow' user access to the 'docker' group
RUN usermod -aG docker airflow

# Check if the 'airflow' group exists, if not, create it
RUN getent group airflow || groupadd airflow

# Ensure the Airflow user owns the home directory
RUN chown -R airflow:airflow /home/airflow || true

# Switch back to the 'airflow' user
USER airflow

# Copy the requirements.txt to the home directory
COPY requirements.txt /home/airflow/requirements.txt

# Install Python dependencies into the virtual environment without '--user'
RUN pip install --no-cache-dir -r /home/airflow/requirements.txt

# Add the local bin to PATH
ENV PATH=/home/airflow/.local/bin:$PATH

# Copy DAGs
COPY dags/ /opt/airflow/dags/
