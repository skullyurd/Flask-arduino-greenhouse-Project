"""
 This program sends data read from a csv file representing humidity, temperature and
 brightness in the form of json requests to a Flask server
"""

from collections import defaultdict
import json
import requests
import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
import statistics

from sqlalchemy import true


DHTPIN  = 12

klux = 0
humidity = 0
temperature = 0

recorded_humidities = [0]
recorded_temperatures = [0]
recorded_klux = [0]

minimal_humidites = 0
minimal_temperatures = 0
minimal_klux = 0

max_humidites = 0
max_temperatures = 0
max_klux = 0

average_humidity = 0
average_temperatures = 0
average_klux = 0

humidity = 0
temperature = 0
lightlevel = 0

average_temperatures = statistics.mean(recorded_temperatures)
def Measure(data):
    global humidity, temperature
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]
        recorded_humidities.append(humidity)
        recorded_temperatures.append(temperature)
        
        
def setup():
    global board
    board = CustomPymata4(com_port = "COM13")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
    board.set_pin_mode_analog_input(2, callback=callback_ldr, differential=50)

def callback_ldr(data):
    global klux
    sensor_value = data[2]
    resistance_sensor = (1023-sensor_value)*10/sensor_value

    klux = 325 * pow(resistance_sensor, -1.4) / 1000
    recorded_klux.append(klux)
    board.displayShow(klux)

def loop():
    global humidity, temperature, klux
    print(humidity, temperature, klux)
    
    while true:
        board.displayShow(klux)
        time.sleep(0.1)
        #calculate the average of the list
        average_humidity = statistics.mean(recorded_humidities)
        average_temperatures = statistics.mean(recorded_temperatures)
        average_klux = statistics.mean(recorded_klux)

        #calculate lowest value
        minimal_humidites = min(recorded_humidities)
        minimal_temperatures = min(recorded_temperatures)
        minimal_klux = min(recorded_klux)

        #calculate highest value
        max_humidites = max(recorded_humidities)
        max_temperatures = max(recorded_temperatures)
        max_klux = max(recorded_klux)

        data = {'current_humidity' : humidity,
        'current_temperature' : temperature, 
        'current_lightlevel' : klux,
        'max_humidity' : max_humidites,
        'max_temperature' : max_temperatures, 
        'max_lightlevel' : max_klux,
        'min_humidity' : minimal_humidites,
        'min_temperature' : minimal_temperatures, 
        'min_lightlevel' : minimal_klux,
        'average_humidity' : average_humidity,
        'average_temperature' : average_temperatures, 
        'average_lightlevel' : average_klux}

        response = requests.post(url, json=data)
        # 200 is OK, other things are errors
        if response.status_code != 200 :
            print (response.text)


url = input("Please enter the IP address of the Flask server [localhost] : ")
if not url:
   url = "http://localhost:5000/post_arduino"
else: 
    url = url + "/post_arduino"
print(f"OK, reading and sending to {url}")
setup()
loop()