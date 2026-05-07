
import logging
import requests
import os
import json
from datetime import datetime
import time

logger = logging.getLogger(__name__)

def extract(url,max_tries,dir):
    """
    This will call the API.
    If there is a server side issue it will retry every 10s for a
    specified number of times.
    Data will be saevd in the specified directory.

    Args:
        url (str): URL to endpoint.
        max_tries (int): Number of times to re-try if there is a server side error.
        dir (str): Directory to save response data to.
    """    
    
    # variables
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    response = requests.get(url)
    data = response.json()

    count = 0


    while count < max_tries:

        if 200 <= response.status_code < 300:

            os.makedirs("data",exist_ok =True)
            filename = f"{dir}/{timestamp}.json"
            with open(filename,"w") as file:
                json.dump(data, file)

            print(f"File {filename} was succesfully created.")
            logger.info(f"File {filename} was succesfully created.")
            return True
            break

        elif response.status_code >= 500:
            #Retry for these status codes after waiting 10sec
            time.sleep(10)
            count +=1
            print(f"Trying again. Attempt {count}")
            logger.info(f"Trying again. Attempt {count}")

        else:
            print(f"Error:{response.status_code} {data.get("message","no message found")}")
            logger.info(f"Error:{response.status_code} {data.get("message","no message found")}")
            break

