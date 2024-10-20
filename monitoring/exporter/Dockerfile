# Dockerfile
FROM python:3.11.9-slim

# Install required Python packages
RUN pip install prometheus_client mlflow

# Copy the exporter script
COPY exporter.py /exporter.py

# Expose port 8000 for Prometheus to scrape metrics
EXPOSE 8000

# Start the exporter
CMD ["python", "/exporter.py"]
