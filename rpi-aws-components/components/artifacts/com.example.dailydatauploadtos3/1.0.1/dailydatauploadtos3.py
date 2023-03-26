import boto3
from botocore.exceptions import NoCredentialsError

AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
BUCKET_NAME = 'YOUR_BUCKET_NAME'
FILE_NAME = 'FILE_NAME.txt'
FILE_PATH = '/path/to/your/FILE_NAME.txt'


def upload_to_s3(file_path, bucket, file_name):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    try:
        s3.upload_file(file_path, bucket, file_name)
        print(f"Upload successful: {file_path} to {bucket}/{file_name}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except NoCredentialsError:
        print("Credentials not available")


if __name__ == '__main__':
    upload_to_s3(FILE_PATH, BUCKET_NAME, FILE_NAME)
