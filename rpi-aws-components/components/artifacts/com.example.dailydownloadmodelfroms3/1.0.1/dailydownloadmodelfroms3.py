"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.dailydownloadmodelfroms3=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.dailydownloadmodelfroms3
"""
import logging
import boto3
import os
import csv
import sqlite3

import datetime

from botocore.exceptions import ClientError

"""
[development purpose]: you need to setup it with yours
cat /root/.aws/credentials
[default]
aws_access_key_id = <your-access-key>
aws_secret_access_key = <your-secret-key>
"""

def download_file():
    now = datetime.datetime.now()
    # Format the date and time as a string in the format "yyyy-mm-dd-H-M-S"
    db_export_file = now.strftime("%Y-%m-%d-%H-%M-%S")

    # Extract only the "yyyy-mm-dd" part of the file name
    db_export_file = db_export_file[:10]

    # os.environ['AWS_SHARED_CREDENTIALS_FILE'] = '/root/.aws/credentials'
    # session = boto3.Session(profile_name='default')

    export_data(db_export_file)
    session = boto3.Session(
        aws_access_key_id='<your-access-key>',
        aws_secret_access_key='<your-aws-secret-access-key>',
    )

    s3_client = session.client('s3')
    try:
        bucket = 'fall-detection-model'
        key = 'fall_detection_model.pkl'
        local_file = '/home/pi/algo-model/fall_detection_model.pkl'
        response = s3_client.download_file(bucket, key, local_file)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

download_file()


