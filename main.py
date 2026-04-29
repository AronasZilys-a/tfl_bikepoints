# Import packages

import requests
import json
import datetime

# variables
url = 'https://api.tfl.gov.uk/BikePoint/Bikepoints_888'

response = requests.get(url)

# print(response)

data = response.json()

timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

file_name = 'Bikepoint_888_'

file_name_time = file_name + timestamp + ".json"



error_message = data.get("message")


if error_message:
    print(f"Error: {response.status_code} {error_message}")
else:
    with open(file_name_time, "w") as file:
        json.dump(data, file)
    print(f"File {file_name_time} was succesfully created! Woohoo")



