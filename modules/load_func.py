
from dotenv import load_dotenv
import boto3
import os
import datetime
import logging
import glob
from pathlib import Path


def load(AWS_KEY_ID,AWS_SECRET_KEY,BUCKET,data_dir):
    """
    This will load any json file in the data directory to a specified s3 bucket.

    Args:
        AWS_KEY_ID (str): access key id attatched to IAM user
        AWS_SECRET_KEY (str): secret access key attatched to IAM user, with relevant permissions
        BUCKET (str): S3 bucket name
        data_dir (str): must be a complete file path for the directory where data is stored e.g.: Path('data')
    """    

    logger = logging.getLogger(__name__)


    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY
    )

    data_dir = Path('data')
    files = list(data_dir.glob('*.json'))

    processed = 0

    for file in files:
        filename = os.path.basename(file)
        try:
            s3_client.upload_file(file,BUCKET,filename)
            logger.info(f'{file} uploaded to s3')
            s3_client.head_object(Bucket=BUCKET,Key=filename)
            os.remove(file)
            logger.info(f'{file} deleted locally')
            processed += 1
        except Exception as e:
            logger.error(e) 

    return(logger.info(f'{processed} files uploaded'))
