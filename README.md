# MLOps Case Study: Machine Learning Model Lifecycle Management

This README provides a detailed walkthrough of the implementation and setup of a Machine Learning model lifecycle management system. This project was developed as a case study for Virtual Minds GmbH's Data Science & Algorithms Team, focusing on storing, scheduling, monitoring, alerting, and serving a machine learning model in a containerized environment.

## **Overview**

The project is divided into several components to achieve complete lifecycle management of a machine learning model:

1. **Model Training and Storage**: Store trained models, persist metadata, and manage versions on Amazon S3.
2. **Scheduled Training**: Train the model daily using Apache Airflow, with defined retries and SLAs.
3. **Model Quality Monitoring**: Track and visualize model metrics using Prometheus and Grafana.
4. **Alerting**: Configure alerts for model staleness and accuracy metrics using Grafana.
5. **Model API**: Serve the model via a REST API built with Flask, which loads the latest available model for prediction.

## **Architecture Diagram**

Below is the architecture diagram depicting all components and their interactions:

![Architecture Diagram](diagram.png)

- **MLflow**: Used for experiment tracking, model versioning, and logging.
- **Amazon S3**: Storage for model artifacts.
- **PostgreSQL**: Database backend for MLflow and Airflow.
- **Airflow**: Orchestrates the training of the model on a daily basis.
- **Prometheus**: Metrics collection for model monitoring.
- **Grafana**: Visualizes the model metrics and triggers alerts.
- **Flask API**: Serves the latest model for predictions via an HTTP endpoint.
- **MailHog**: Email testing tool used for alert notifications.

## **System Components**

### **1. Model Training and Storage**

- **Model Training**: The training process uses a simple machine learning model based on the Iris dataset. The model is trained with hyperparameters which are also logged.
- **Model Storage**: Trained models are versioned and saved to an Amazon S3 bucket using **MLflow**. Each model version contains metadata such as training accuracy, hyperparameters, and the unique timestamp at which it was trained.
- **MLflow**: Tracks and logs metrics, parameters, and artifacts (model versions). This project uses MLflow with PostgreSQL as the backend database to store tracking metadata.

### **2. Scheduled Model Training with Airflow**

- **Apache Airflow** is used for scheduling model training daily.
- **DAG Configuration**: Airflow DAG schedules the training script with multiple retries if a failure occurs.
- **SLA and Retries**: The Airflow DAG ensures training completes within a specified SLA and retries the task if something goes wrong.

### **3. Model Quality Monitoring with Prometheus and Grafana**

- **Prometheus**: Used for collecting metrics such as training and evaluation accuracy.
- **Grafana**: Displays time-series data for model accuracy and metrics like "Training Accuracy Score" and "Model Accuracy" in dedicated dashboards.
- **Panels**: Panels are set up for real-time monitoring of model metrics and visualizing the average accuracy of the last 7 days.

### **4. Alerting with Grafana**

- **Grafana Alerting**: Configured to alert if the latest model is older than 36 hours or if the model accuracy falls below a certain threshold.
- **Email Notifications**: Alerts are sent to configured email addresses using **MailHog** as a local SMTP server.
- **Provisioning**: All dashboards and alert rules are automatically created using JSON provisioning files.

### **5. Model Serving via Flask API**

- **REST API**: A Flask-based REST API is developed to serve the latest trained model.
- **Automatic Model Update**: The API automatically loads the latest available model from MLflow every 60 seconds to ensure the latest version is used.
- **Prediction Endpoint**: Accepts input vectors via a POST request and returns predictions.

## **Directory Structure**

```
.
├── README.md
├── docker-compose.yml
├── postgres-init.sql
├── orchestration/                  # Airflow related files
├── monitoring/
│   ├── prometheus/
│   │   └── prometheus.yml         # Prometheus configuration
│   ├── grafana/
│   │   ├── provisioning/
│   │   │   ├── datasources/       # Datasource configuration for Grafana
│   │   │   ├── dashboards/        # Dashboard configuration for Grafana
│   │   │   └── alerting/          # Alert rules for Grafana
│   └── exporter/
├── serving/
│   ├── app.py                     # Flask API for serving the model
│   ├── requirements.txt           # Python requirements for Flask app
│   └── Dockerfile                 # Dockerfile for model-serving API
└── mlflow/
    └── Dockerfile                 # Dockerfile for MLflow server
```

## **Setup and Installation Instructions**

### **1. Prerequisites**

- **Docker** and **Docker Compose** are required for running the entire system.
- **AWS Credentials** for S3 access should be configured in `~/.aws/credentials`.
- **AWS IAM Roles**: Reviewer roles are set up to manage and configure the project.

### **2. Environment Configuration**

- **AWS Setup**: Ensure the AWS credentials are available in `~/.aws/credentials` for accessing S3.
- **PostgreSQL Initialization**: PostgreSQL databases and users for MLflow and Airflow are created using the `postgres-init.sql` file.
- **AWS IAM Roles**: Reviewer roles have been set up to provide access for configuration and management. Ensure the roles are configured with the necessary permissions for managing S3, databases, and other AWS resources.

**Example IAM Policy for Reviewers**:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "rds:*",
        "secretsmanager:GetSecretValue",
        "iam:PassRole"
      ],
      "Resource": "*"
    }
  ]
}
```

### **3. Running the System**

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/bilalimamoglu/ml-lifecycle-system.git
   cd ml-lifecycle-system
   ```

2. **Build and Start Services**:

   Use Docker Compose to build and start all services:

   ```sh
   docker-compose up -d --build
   ```

3. **Initialize PostgreSQL Databases**:

   The `postgres-init.sql` file is automatically executed to create the required users and databases for MLflow and Airflow.

4. **Access the Components**:

   - **MLflow UI**: [http://localhost:5000](http://localhost:5000)
   - **Airflow UI**: [http://localhost:8080](http://localhost:8080) (username: `airflow`, password: `airflow`)
   - **Grafana UI**: [http://localhost:3000](http://localhost:3000) (username: `admin`, password: `admin`)
   - **MailHog**: [http://localhost:8025](http://localhost:8025) for email notifications
   - **Flask API**: [http://localhost:5001](http://localhost:5001)

### **4. Model Training and Storage**

- The model is trained and stored automatically as per the daily schedule defined in **Airflow**.
- Models are saved to **S3** with all metadata and metrics logged via **MLflow**.
- **Accessing S3 Bucket**: To view the stored models, log in to your AWS account and navigate to the S3 service. Search for the bucket named `mlflow-artifacts-bilalimg` to see all model artifacts.

### **5. Predicting with the Model API**

- Send a POST request to the `/predict` endpoint of the Flask API to receive predictions.

  **Example Request**:

  ```sh
  curl -X POST -H "Content-Type: application/json" \
  -d '{"sepal length (cm)": 5.1, "sepal width (cm)": 3.5, "petal length (cm)": 1.4, "petal width (cm)": 0.2}' \
  http://localhost:5001/predict
  ```

  **Expected Response**:

  ```json
  {
    "prediction": [0]
  }
  ```

### **6. Alerting and Monitoring**

- **Grafana Dashboards**: Automatically configured to display real-time metrics such as training accuracy and model accuracy over time.
- **Alerts**: Configured using **Grafana Alerting**, with alerts sent via **MailHog**.

### **7. Reviewer IAM Role Configuration**

- **AWS IAM Roles**: Reviewer roles have been set up to enable reviewers to configure the environment and manage resources. These roles include permissions to access S3 buckets, manage RDS instances, and access secrets stored in AWS Secrets Manager.
- **Accessing AWS IAM Role**: Use your AWS Management Console to assume the reviewer role by selecting "Switch Role" and entering the required information to assume the reviewer permissions.

### **8. Troubleshooting**

- **Port Conflicts**: Ensure no services are already using ports `5000`, `5001`, `8080`, `3000`, or `8025`.
- **Database Connection Issues**: Check the PostgreSQL logs if you encounter connection issues.
  
  ```sh
  docker-compose logs postgres
  ```

- **Model Not Loading in API**: Check the `model-serving` container logs to debug model-loading issues.

  ```sh
  docker-compose logs model-serving
  ```

## **Contributing**

Feel free to fork the repository and create pull requests for improvements. Contributions are always welcome.

## **Contact Information**

If you have questions or need further assistance, you can reach out to **Virtual Minds GmbH** or contact the project contributors.
