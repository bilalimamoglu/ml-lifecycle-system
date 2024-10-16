
from dependencies import get_boto_client



def write_s3(model):
    client=get_boto_client(service_name='s3')
