import logging
import boto3
from botocore.exceptions import ClientError


def upload_file(file_name):
    s3_client = boto3.client('s3')
    try:
        bucket = 'fall-detection-daily-data-bucket'
        response = s3_client.upload_file(file_name, bucket, file_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True


upload_file('test.csv')
