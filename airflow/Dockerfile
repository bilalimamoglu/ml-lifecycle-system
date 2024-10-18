# Use the official Airflow image as the base
FROM apache/airflow:2.10.2-python3.11

# Switch to root to install system dependencies
USER root

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Accept the Docker group GID as a build argument, default to 999 if not provided
ARG DOCKER_GID=999

# Create the docker group with the specified GID
RUN groupadd -g ${DOCKER_GID} docker || true

# Add the 'airflow' user to the docker group
RUN usermod -aG docker airflow

# Ensure the Airflow user owns the home directory
RUN chown -R airflow:airflow /home/airflow || true

# Copy the entrypoint script and give execution permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch back to the 'airflow' user
USER airflow

# Copy the requirements.txt to the home directory
COPY requirements.txt /home/airflow/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /home/airflow/requirements.txt

# Add the local bin to PATH
ENV PATH=/home/airflow/.local/bin:$PATH

# Copy DAGs
COPY dags/ /opt/airflow/dags/

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
