"""
 This program sends data read from a csv file representing humidity, temperature and
 brightness in the form of json requests to a Flask server
"""

from collections import defaultdict
import json
import csv
import requests

filelines = []
columns = defaultdict(list)

input_file = "sensor_log_with_id.csv" #tries to find a file with this name that is supposed to be in the same map as the script
url = input("Please enter the IP address of the Flask server [localhost] : ")
if not url:
   url = "http://localhost:5000/post_data"
else: 
    url = url + "/post_data"
print(f"OK, reading from {input_file} and sending to {url}")
with open(input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        filelines.append(row)

        for(k, v) in row.items():
            columns[k].append(v)


    data = {'listID' : columns['sensor_id'],
            'listTime' : columns['time_stamp'],
            'listHumidity' : columns['humidity'],
            'listTemperature' : columns['temperature'],
            'listBrightness' : columns['brightness'],
            'allRows' : filelines}

    response = requests.post(url, json=data)
    # 200 is OK, other things are errors
    if response.status_code != 200 :
        print (response.text)