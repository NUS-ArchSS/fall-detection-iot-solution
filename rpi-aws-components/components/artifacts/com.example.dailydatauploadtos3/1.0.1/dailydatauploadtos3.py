"""
sudo /greengrass/v2/bin/greengrass-cli deployment create --recipeDir ~/fall-detection-iot-solution/rpi-aws-components/components/recipe/ --artifactDir ~/fall-detection-iot-solution/rpi-aws-components/components/artifacts/ --merge "com.example.dailydatauploadtos3=1.0.1"
sudo /greengrass/v2/bin/greengrass-cli deployment create --remove com.example.dailydatauploadtos3
"""
import logging
import boto3
import os
import csv
import sqlite3

import datetime

from botocore.exceptions import ClientError


def export_data(file_name):
    conn = sqlite3.connect('/tmp/sensor_data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM sensor_data')
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Open a CSV file for writing
    with open(file_name, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the column names to the CSV file
        writer.writerow(['mag_x', 'mag_y', 'mag_z', 'acc_x', 'acc_y', 'acc_z', 'create_timestamp', 'result'])

        # Write the data to the CSV file
        for row in data:
            print(row)
            writer.writerow(row)

"""
[development purpose]: you need to setup it with yours
cat /root/.aws/credentials
[default]
aws_access_key_id = <your-access-key>
aws_secret_access_key = <your-secret-key>
"""

def upload_file():
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
        aws_secret_access_key='<your-secret-key>',
    )

    s3_client = session.client('s3')
    try:
        bucket = 'fall-detection-daily-data-bucket'
        response = s3_client.upload_file(db_export_file, bucket, db_export_file)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file()


