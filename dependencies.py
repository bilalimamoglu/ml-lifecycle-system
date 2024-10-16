

from typing import Annotated, Dict
from config import settings
import boto3
from botocore.exceptions import ClientError



def get_boto_client(service_name):
    cognito_client = boto3.client(service_name,
                                  aws_access_key_id=settings.Access_Key_ID_Reviewer,
                                  aws_secret_access_key=settings.Secret_Access_Key_Reviewer,
                                  region_name=settings.AWS_DEFAULT_REGION)

    return cognito_client
