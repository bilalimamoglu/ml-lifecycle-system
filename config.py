import boto3
import json
import logging
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the ML Lifecycle Management System.

    The settings are loaded dynamically from AWS Secrets Manager.
    """

    def get_secret(self):
        """
        Fetch the secret from AWS Secrets Manager.
        """
        secret_name = "ml-lifecycle-secrets"
        region_name = "eu-central-1"  # Replace with your region

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=region_name,
        )

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except Exception as e:
            logging.error(f"Failed to retrieve secret: {e}")
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)

    def __init__(self):
        """
        Initialize settings by loading the secrets.
        """
        secrets = self.get_secret()

        # Set attributes from secrets
        self.AWS_ACCESS_KEY_ID = secrets["AWS_ACCESS_KEY_ID"]
        self.AWS_SECRET_ACCESS_KEY = secrets["AWS_SECRET_ACCESS_KEY"]
        self.AWS_DEFAULT_REGION = secrets.get("AWS_DEFAULT_REGION", "eu-central-1")
        self.S3_BUCKET_NAME = secrets["S3_BUCKET_NAME"]
        self.MLFLOW_TRACKING_URI = "http://mlflow-server:5000"

        # Set up logging configuration
        logging.basicConfig(
            level=logging.INFO,  # Change to DEBUG for more detailed logs
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )


# Instantiate the settings
settings = Settings()

# You can now access the settings like this:
# print(settings.AWS_ACCESS_KEY_ID)
# print(settings.S3_BUCKET_NAME)
