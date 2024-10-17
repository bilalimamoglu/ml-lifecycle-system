FROM python:3.11.9-slim

# Install dependencies
RUN pip install --no-cache-dir mlflow boto3 requests prometheus_client

# Copy exporter script
COPY exporter.py /exporter.py

# Add test script
COPY test_exporter.py /test_exporter.py

# Start exporter and run test script after a delay
CMD ["sh", "-c", "python /exporter.py & sleep 10 && python /test_exporter.py && wait"]
