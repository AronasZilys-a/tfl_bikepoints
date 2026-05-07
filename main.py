
from modules.extract_func import extract
from modules.setup_logging import setup_logging
from modules.load_func import load
from pathlib import Path
import os
from dotenv import load_dotenv



logger = setup_logging('logs')
logger.info('Logger Initialised')

url = 'https://api.tfl.gov.uk/BikePoint'

load_dotenv()

AWS_KEY_ID = os.getenv('AWS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET = os.getenv('BUCKET')



if extract(url,3,'data'):
    data_dir = Path('data')
    load(AWS_KEY_ID,AWS_SECRET_KEY,BUCKET,data_dir)
    logger.info('Script ran successfully')
else:
    logger.error('Extract failed so script termianted')