from pydantic_settings import BaseSettings
import logging
from pathlib import Path
import os

# Get the current file path
current_file_path = Path(__file__).resolve()
from decouple import config


class Settings(BaseSettings):
    """
    Configuration settings for the Table API.

    The settings are loaded from environment variables defined in a `.env` file.
    This class uses `pydantic.BaseSettings`, which automatically reads the environment
    variables, providing a simple and clean way to manage configuration.

    Attributes:
        PROJECT_NAME (str): The name of the project, default is "Table API".
        PROJECT_VERSION (str): The version of the project, default is "1.0.0".
        OPENAI_API_KEY (str): The API key for accessing OpenAI services.
        QDRANT_HOST (str): The hostname for the Qdrant vector database.
        QDRANT_PORT (int): The port number for the Qdrant vector database.
        STORAGE_TYPE (str): The type of storage being used, e.g., local or S3.
        LOCAL_STORAGE_PATH (str): The path for storing files locally, default is "./local_storage".
        S3_BUCKET_NAME (str): The name of the S3 bucket to be used for storage, optional.
        AWS_ACCESS_KEY_ID (str): The AWS access key ID, required if using S3.
        AWS_SECRET_ACCESS_KEY (str): The AWS secret access key, required if using S3.
    """


    # AWS Cognito Boto client keys
    Access_Key_ID_Reviewer: str = config("Access_Key_ID_Reviewer")
    Secret_Access_Key_Reviewer: str = config("Secret_Access_Key_Reviewer")
    AWS_DEFAULT_REGION='eu-central-1'
    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Change to DEBUG for more detailed logs
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


# Instantiate the settings
settings = Settings()
