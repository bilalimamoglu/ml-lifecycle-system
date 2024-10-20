# Dockerfile
FROM python:3.11.9-slim

RUN pip install prometheus_client mlflow

COPY exporter.py /exporter.py

CMD ["python", "/exporter.py"]
