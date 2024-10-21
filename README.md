# Machine Learning Model Lifecycle Management System

This comprehensive guide walks you through the implementation of a Machine Learning Model Lifecycle Management System. The project is designed to address the complete lifecycle of a machine learning model, from training and storage to monitoring, alerting, and serving predictions via an API. The system leverages various AWS services, containerization with Docker, orchestration with Airflow, and monitoring tools like Prometheus and Grafana.

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [AWS Setup](#aws-setup)
  - [S3 Bucket Configuration](#s3-bucket-configuration)
  - [IAM Users and Roles](#iam-users-and-roles)
  - [AWS Secrets Manager](#aws-secrets-manager)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
  - [Prerequisites](#prerequisites)
  - [AWS CLI Configuration](#aws-cli-configuration)
  - [Setting Up AWS IAM Users and Policies](#setting-up-aws-iam-users-and-policies)
  - [Setting Up S3 Bucket](#setting-up-s3-bucket)
  - [Setting Up AWS Secrets Manager](#setting-up-aws-secrets-manager)
- [MLflow Integration](#mlflow-integration)
  - [Configuring MLflow with S3](#configuring-mlflow-with-s3)
- [Airflow Setup](#airflow-setup)
  - [Docker and Docker Compose](#docker-and-docker-compose)
  - [Airflow DAGs and Tasks](#airflow-dags-and-tasks)
- [Monitoring and Alerting](#monitoring-and-alerting)
  - [Prometheus Configuration](#prometheus-configuration)
  - [Grafana Dashboard and Alerts](#grafana-dashboard-and-alerts)
- [Model Serving via API](#model-serving-via-api)
  - [Flask API Implementation](#flask-api-implementation)
  - [Model Update Mechanism](#model-update-mechanism)
- [Running the Project](#running-the-project)
- [Edge Cases and Testing](#edge-cases-and-testing)
- [Conclusion](#conclusion)
- [Contact Information](#contact-information)

---

## Introduction

The goal of this project is to implement a complete Machine Learning Model Lifecycle Management System that includes:

1. **Model Training and Storage**: Automate the training process and store models with unique versions, hyperparameters, and accuracy metrics.
2. **Scheduled Training**: Schedule daily training with retries and SLAs using Apache Airflow.
3. **Model Monitoring**: Visualize accuracy over time and display average accuracy using Prometheus and Grafana.
4. **Alerting Mechanisms**: Set up alerts for model staleness and accuracy thresholds.
5. **Model Serving**: Provide an API endpoint for predictions, which automatically pulls the latest model.

This project is containerized using Docker and orchestrated with Docker Compose, allowing for easy deployment and scalability.

---

## Architecture Overview

The system architecture comprises several interconnected components:

1. **AWS Services**:
   - **S3 Bucket**: Stores MLflow artifacts, including model versions and metrics.
   - **IAM Users and Roles**: Manages access to AWS resources securely.
   - **AWS Secrets Manager**: Stores sensitive information like AWS credentials and S3 bucket names.

2. **Machine Learning Components**:
   - **MLflow**: Handles experiment tracking, model versioning, and artifact storage.
   - **Airflow**: Orchestrates scheduled training tasks with retries and SLAs.
   - **Flask API**: Serves the latest model for predictions via a RESTful interface.

3. **Monitoring and Alerting Tools**:
   - **Prometheus**: Collects and stores metrics for monitoring model performance.
   - **Grafana**: Visualizes metrics and sets up alerting rules.

4. **Containerization and Orchestration**:
   - **Docker**: Containerizes applications for consistent deployment environments.
   - **Docker Compose**: Orchestrates multi-container applications, simplifying the setup process.

### Component Interaction Flow

1. **Model Training**:
   - Airflow triggers the model training DAG daily.
   - The training script logs metrics and parameters to MLflow.
   - Trained models and artifacts are stored in the S3 bucket via MLflow.

2. **Model Monitoring**:
   - Prometheus scrapes metrics from the MLflow exporter.
   - Grafana visualizes these metrics and calculates averages over time.
   - Alerts are configured in Grafana to monitor specific conditions.

3. **Model Serving**:
   - The Flask API loads the latest model from MLflow.
   - Clients can request predictions via the API endpoint.
   - The API automatically updates the model if a new version is available.

---

## AWS Setup

### S3 Bucket Configuration

**Bucket Name**: `mlflow-artifacts-bilalimg`

- **Purpose**: Stores MLflow artifacts such as models, metrics, and parameters.
- **Configuration Steps**:
  - Created an S3 bucket with a unique name.
  - Configured bucket policies to allow access only to authorized IAM users and roles.
  - Enabled versioning to keep track of model versions.

**Reasoning**: S3 provides scalable, secure, and durable storage for artifacts. It integrates seamlessly with MLflow for artifact storage.

### IAM Users and Roles

#### IAM Users

1. **cli-user**:
   - **Purpose**: Used for AWS CLI interactions, such as uploading artifacts to S3.
   - **Permissions**: Granted programmatic access to S3, Lambda, and other necessary services.

2. **reviewer-user**:
   - **Purpose**: Provides read-only access for code reviewers.
   - **Permissions**: Limited to viewing resources without the ability to modify them.

#### IAM Group

- **Group Name**: `ml-lifecycle`
- **Purpose**: Manages permissions for users involved in the ML lifecycle project.
- **Policy Attached**: `ml-lifecycle-policy`

#### IAM Policy (`ml-lifecycle-policy`)

- **Permissions**:
  - **S3**: Full access to the specified S3 bucket for reading and writing artifacts.
  - **Lambda**: Permissions to invoke and manage Lambda functions if needed.
  - **Secrets Manager**: Access to retrieve secrets necessary for the application.
  - **SNS**: Permissions to publish notifications for alerts.

**Reasoning**: Using IAM users and groups with appropriate policies ensures secure and organized access management, adhering to the principle of least privilege.

### AWS Secrets Manager

- **Secret Name**: `ml-lifecycle-secrets`
- **Purpose**: Securely stores sensitive information like AWS credentials and the S3 bucket name.
- **Stored Secrets**:
  - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` for `cli-user`.
  - `S3_BUCKET_NAME` set to `mlflow-artifacts-bilalimg`.
- **Configuration**:
  - The application is configured to fetch secrets dynamically at runtime.
  - Ensures that sensitive information is not hard-coded or exposed in the codebase.

**Reasoning**: AWS Secrets Manager provides a secure way to handle sensitive data, reducing the risk of credential leakage.

---

## Project Structure

The project is organized into directories and files as follows:

```
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── setup_aws_env.sh
├── requirements.txt
├── postgres-init.sql
├── mlflow/
│   └── Dockerfile
├── orchestration/
│   ├── dags/
│   │   ├── __init__.py
│   │   └── daily_model_training.py
│   └── python_scripts/
│       ├── __init__.py
│       ├── data_generation.py
│       ├── data_preprocessing.py
│       ├── model_training.py
│       └── model_evaluation.py
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml
│   ├── grafana/
│   │   ├── provisioning/
│   │   │   ├── datasources/
│   │   │   │   └── datasources.yaml
│   │   │   ├── dashboards/
│   │   │   │   └── dashboards.yaml
│   │   │   └── alerting/
│   │   │       └── alerting.yaml
│   │   └── dashboards/
│   │       └── ml_model_metrics.json
│   └── exporter/
│       ├── Dockerfile
│       └── exporter.py
├── serving/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── data/
    └── (Data files generated during runtime)
```

### Explanation of Key Directories and Files

- **Dockerfile**: Base Dockerfile for the project.
- **docker-compose.yml**: Orchestrates all services using Docker Compose.
- **setup_aws_env.sh**: Script to set up AWS environment variables and credentials.
- **requirements.txt**: Lists Python dependencies.
- **postgres-init.sql**: Initializes PostgreSQL databases for Airflow and MLflow.
- **mlflow/**: Contains Dockerfile for the MLflow server.
- **orchestration/**: Airflow-related files.
  - **dags/**: Contains Airflow DAG definitions.
  - **python_scripts/**: Python scripts for data generation, preprocessing, training, and evaluation.
- **monitoring/**: Configuration for Prometheus and Grafana.
  - **prometheus/**: Prometheus configuration files.
  - **grafana/**: Grafana provisioning files for datasources, dashboards, and alerts.
  - **exporter/**: Custom exporter to expose MLflow metrics to Prometheus.
- **serving/**: Flask API for serving the model.
- **data/**: Stores generated data and split datasets.

---

## Environment Setup

### Prerequisites

- **Operating System**: Linux-based OS is recommended.
- **Docker**: Ensure Docker is installed and running.
- **Docker Compose**: Version compatible with Docker.
- **AWS Account**: Access to AWS services with necessary permissions.
- **AWS CLI**: Installed and configured.

### AWS CLI Configuration

1. **Install AWS CLI**:

   ```sh
   pip install awscli
   ```

2. **Configure AWS CLI**:

   ```sh
   aws configure
   ```

   Provide the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DEFAULT_REGION`, and `DEFAULT_OUTPUT_FORMAT` when prompted.

### Setting Up AWS IAM Users and Policies

#### Creating IAM Users

1. **cli-user**:

   - Navigate to AWS IAM console.
   - Create a new user named `cli-user`.
   - Assign programmatic access.
   - Attach the `ml-lifecycle-policy`.

2. **reviewer-user**:

   - Create a new user named `reviewer-user`.
   - Assign appropriate read-only permissions.

#### Creating IAM Group and Policy

1. **Create IAM Group**:

   - Name: `ml-lifecycle`
   - Add `cli-user` and `reviewer-user` to this group.

2. **Create IAM Policy** (`ml-lifecycle-policy`):

   - Permissions:
     - `S3`: Full access to `mlflow-artifacts-bilalimg` bucket.
     - `SecretsManager`: Read access to `ml-lifecycle-secrets`.
     - `SNS`, `Lambda`: Access as required.
   - Attach this policy to the `ml-lifecycle` group.

**Reasoning**: Grouping users simplifies permission management and ensures consistent access controls.

### Setting Up S3 Bucket

1. **Create S3 Bucket**:

   - Name: `mlflow-artifacts-bilalimg`.
   - Enable versioning to keep track of different model versions.
   - Set up bucket policies to restrict access to authorized IAM users.

2. **Configure Bucket Permissions**:

   - Ensure that only `cli-user` and services assume roles with access to this bucket.
   - Block public access to the bucket.

**Reasoning**: Secure storage of artifacts is crucial. Versioning allows for tracking and rolling back to previous models if necessary.

### Setting Up AWS Secrets Manager

1. **Create Secret**:

   - Name: `ml-lifecycle-secrets`.
   - Store the following key-value pairs:
     - `AWS_ACCESS_KEY_ID`: `[Your AWS Access Key ID]`
     - `AWS_SECRET_ACCESS_KEY`: `[Your AWS Secret Access Key]`
     - `S3_BUCKET_NAME`: `mlflow-artifacts-bilalimg`

2. **Configure Access**:

   - Ensure that only authorized IAM roles and users can retrieve this secret.

**Reasoning**: Centralized management of sensitive information enhances security and simplifies secret rotation.

---

## MLflow Integration

### Configuring MLflow with S3

1. **MLflow Tracking Server**:

   - Located in the `mlflow/` directory.
   - **Dockerfile**:

     ```dockerfile
     FROM python:3.11.9-slim
     RUN pip install mlflow boto3 psycopg2-binary
     EXPOSE 5000
     CMD ["mlflow", "server", "--host", "0.0.0.0"]
     ```

2. **Environment Variables**:

   - `MLFLOW_S3_ENDPOINT_URL`: `https://s3.amazonaws.com`
   - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`: Retrieved from AWS Secrets Manager or environment variables.
   - `MLFLOW_BACKEND_STORE_URI`: `postgresql+psycopg2://mlflow:mlflow@postgres:5432/mlflow`
   - `MLFLOW_DEFAULT_ARTIFACT_ROOT`: `s3://mlflow-artifacts-bilalimg/`

3. **Docker Compose Configuration**:

   - Service Name: `mlflow-server`
   - Depends on `postgres` service for backend storage.

**Reasoning**: Using S3 as the artifact store allows for scalable storage. PostgreSQL serves as a reliable backend for MLflow's tracking data.

---

## Airflow Setup

### Docker and Docker Compose

- **Airflow Image**: Customized in `orchestration/` directory.
- **Dockerfile**:

  ```dockerfile
  FROM apache/airflow:2.5.1
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY dags/ /opt/airflow/dags/
  COPY python_scripts/ /opt/airflow/python_scripts/
  ```

- **Environment Variables**:

  - `AIRFLOW__DATABASE__SQL_ALCHEMY_CONN`: Connection string to PostgreSQL.
  - `MLFLOW_TRACKING_URI`: `http://mlflow-server:5000`
  - AWS credentials are set via environment variables or mounted from the host.

- **Docker Compose Service**: `airflow`

### Airflow DAGs and Tasks

- **DAG File**: `orchestration/dags/daily_model_training.py`
- **Tasks**:

  1. **generate_data**:
     - Generates the Iris dataset and saves it to `data/iris.csv`.
     - **Why**: Ensures fresh data is used for each training cycle.

  2. **preprocess_data**:
     - Splits data into training and testing sets.
     - **Why**: Preprocessing is essential for model performance.

  3. **train_model**:
     - Trains a Random Forest model with random hyperparameters.
     - Logs parameters and metrics to MLflow.
     - **Why**: Introduces variability and tests the system's ability to handle different model versions.

  4. **evaluate_model**:
     - Evaluates the trained model on the test set.
     - Logs accuracy to MLflow.
     - **Why**: Monitoring model performance over time is crucial.

- **Retries and SLAs**:

  - Configured in `default_args` of the DAG.
  - Retries set to `1` with a delay of `5` minutes.
  - **Why**: Ensures robustness in case of transient failures.

---

## Monitoring and Alerting

### Prometheus Configuration

- **Configuration File**: `monitoring/prometheus/prometheus.yml`
- **Scrape Configs**:

  ```yaml
  scrape_configs:
    - job_name: 'exporter'
      static_configs:
        - targets: ['exporter:8000']
  ```

- **Exporter**:

  - Custom exporter located in `monitoring/exporter/`.
  - Exposes MLflow metrics such as `model_accuracy` and `training_accuracy_score`.
  - **Dockerfile**:

    ```dockerfile
    FROM python:3.11.9-slim
    RUN pip install prometheus_client mlflow
    COPY exporter.py /exporter.py
    EXPOSE 8000
    CMD ["python", "/exporter.py"]
    ```

**Reasoning**: Prometheus collects metrics at regular intervals, enabling real-time monitoring and alerting.

### Grafana Dashboard and Alerts

- **Provisioning**:

  - Dashboards, datasources, and alerting rules are provisioned using configuration files in `monitoring/grafana/provisioning/`.

- **Datasources**:

  - Configured in `datasources.yaml` to point to the Prometheus instance.

- **Dashboard**:

  - JSON file `ml_model_metrics.json` defines panels for:

    - **Model Accuracy Over Time**: Displays `model_accuracy` metric.
    - **Training Accuracy Score**: Shows `training_accuracy_score`.

- **Alerts**:

  - Configured in `alerting.yaml`.
  - **Alert Conditions**:

    - **Low Model Accuracy**:
      - Triggers if `model_accuracy` falls below `0.99`.
      - Evaluated over the last `5` minutes.

    - **Model Staleness**:
      - Triggers if the model hasn't been updated in the last `36` hours.
      - Uses `model_last_updated` metric from the exporter.

- **Notifications**:

  - Alerts are sent via email using **MailHog**, a local SMTP server for testing.

**Reasoning**: Grafana provides a user-friendly interface for visualizing metrics and setting up complex alerting rules.

---

## Model Serving via API

### Flask API Implementation

- **Location**: `serving/app.py`
- **Functionality**:

  - Provides a `/predict` endpoint that accepts input features in JSON format.
  - Returns predictions based on the latest model.

- **Dockerfile**:

  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY app.py .
  ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000
  CMD ["python", "app.py"]
  ```

- **Requirements**:

  ```txt
  flask
  mlflow
  pandas
  scikit-learn
  threading
  ```

### Model Update Mechanism

- **Model Update Daemon**:

  - A background thread checks for new model versions every `60` seconds.
  - Loads the latest model from MLflow if a new version is available.

- **Why Not Use Model Registry**:

  - Chose simplicity over setting up MLflow Model Registry.
  - Directly querying the latest run ensures the most recent model is used without additional configuration.

**Reasoning**: Automating model updates ensures that the API always serves the latest model without manual intervention.

---

## Running the Project

### Step-by-Step Instructions

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/bilalimamoglu/ml-lifecycle-system.git
   cd ml-lifecycle-system
   ```

2. **Set Up AWS Credentials**:

   - Run the `setup_aws_env.sh` script to copy AWS credentials to the project directory:

     ```sh
     ./setup_aws_env.sh
     ```

   - **Note**: Ensure that your AWS credentials are correctly set in `~/.aws/credentials`.

3. **Initialize PostgreSQL Databases**:

   - The `postgres-init.sql` file will automatically create the necessary databases and users when the PostgreSQL container starts.

4. **Build and Start Services**:

   - Use Docker Compose to build and run all services:

     ```sh
     docker-compose up -d --build
     ```

5. **Access the Web Interfaces**:

   - **Airflow**: [http://localhost:8080](http://localhost:8080) (Username: `airflow`, Password: `airflow`)
   - **MLflow**: [http://localhost:5000](http://localhost:5000)
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (Username: `admin`, Password: `admin`)
   - **MailHog**: [http://localhost:8025](http://localhost:8025)
   - **Model API**: [http://localhost:5001](http://localhost:5001)

6. **Trigger the Airflow DAG**:

   - In the Airflow UI, manually trigger the `daily_model_training` DAG to start the initial training process.

7. **Verify Model Training**:

   - Check the MLflow UI to verify that a new run has been logged.
   - Ensure that model artifacts are stored in the S3 bucket.

8. **Test the Model API**:

   - Send a POST request to the `/predict` endpoint:

     ```sh
     curl -X POST -H "Content-Type: application/json" \
     -d '{"sepal length (cm)": 5.1, "sepal width (cm)": 3.5, "petal length (cm)": 1.4, "petal width (cm)": 0.2}' \
     http://localhost:5001/predict
     ```

   - Expected Response:

     ```json
     {
       "prediction": ["setosa"]
     }
     ```

9. **Monitor Metrics and Alerts**:

   - In Grafana, view the **ML Model Metrics Dashboard**.
   - Check for any alerts in the **Alerting** section.
   - Use MailHog to view any email notifications triggered by alerts.

---

## Edge Cases and Testing

### Potential Issues and Handling

1. **AWS Credentials Not Found**:

   - **Symptom**: Errors related to missing AWS credentials.
   - **Solution**: Ensure that AWS credentials are correctly configured and accessible to the containers.

2. **Model Not Loading in API**:

   - **Symptom**: API returns "Model not loaded" error.
   - **Solution**: Verify that the model exists in MLflow and that the API has network access to the MLflow server.

3. **Airflow Task Failures**:

   - **Symptom**: Airflow tasks fail due to various errors.
   - **Solution**:
     - Check task logs in Airflow UI for error details.
     - Ensure that all dependencies are installed.
     - Verify network connectivity between Airflow and MLflow.

4. **Prometheus Metrics Not Available**:

   - **Symptom**: Grafana panels show "No data".
   - **Solution**:
     - Verify that the exporter is running and accessible.
     - Check Prometheus configuration and logs.

5. **Alerts Not Triggering**:

   - **Symptom**: Expected alerts are not appearing.
   - **Solution**:
     - Check Grafana alert rules for correctness.
     - Ensure that notification channels are properly configured.

### Testing Scenarios

1. **Model Staleness**:

   - **Test**: Stop the Airflow scheduler and wait for 36 hours (or adjust the alert threshold for testing).
   - **Expected Outcome**: Alert is triggered for model staleness.

2. **Low Accuracy**:

   - **Test**: Modify the training script to produce a low-accuracy model.
   - **Expected Outcome**: Alert is triggered when accuracy falls below the threshold.

3. **API Prediction Validity**:

   - **Test**: Send invalid input data to the `/predict` endpoint.
   - **Expected Outcome**: API returns an error with appropriate status code.

**Reasoning**: Testing edge cases ensures that the system is robust and can handle unexpected scenarios gracefully.

---

## Conclusion

This project demonstrates a complete machine learning lifecycle management system, integrating various technologies to handle model training, storage, monitoring, alerting, and serving. By leveraging AWS services, containerization, and orchestration tools, we achieve a scalable and maintainable architecture.

**Key Takeaways**:

- **Secure and Scalable Storage**: Using AWS S3 and IAM roles ensures data security and scalability.
- **Automated Training and Deployment**: Airflow automates model training with retries and SLAs.
- **Real-time Monitoring and Alerting**: Prometheus and Grafana provide insights into model performance and system health.
- **Continuous Model Serving**: The API ensures that the latest model is always available for predictions.

**Future Improvements**:

- Implementing CI/CD pipelines for automated deployments.
- Enhancing security by integrating AWS KMS for key management.
- Scaling the API using a production-ready server like Gunicorn or uWSGI.

---

## Contact Information

For any questions or further assistance, please contact:

- **Name**: Bilal Imamoglu
- **Email**: [bilal@example.com](mailto:bilal@example.com)
- **GitHub**: [github.com/bilalimamoglu](https://github.com/bilalimamoglu)

---

**Note**: This project was developed as a case study for Virtual Minds GmbH's Data Science & Algorithms Team.