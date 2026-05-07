
from dotenv import load_dotenv
import boto3
import os
import datetime
import logging
import glob
from pathlib import Path

log_dir = "logs"
os.makedirs(log_dir,exist_ok=True)
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filename = f"{log_dir}/load_{timestamp}.log"

logging.basicConfig(
    filename=log_filename,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    level= logging.INFO
)

logger = logging.getLogger()
logger.info('Logger initialised')




load_dotenv()

AWS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET = os.getenv('BUCKET')

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

logger.info(f'{processed} files uploaded')


