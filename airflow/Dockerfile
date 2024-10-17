FROM apache/airflow:2.10.2-python3.11

# Install additional Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs
COPY dags/ /opt/airflow/dags/
