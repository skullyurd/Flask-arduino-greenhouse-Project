from flask import Flask, jsonify, request, render_template, template_rendered
import json
from datetime import date, datetime
import requests
import statistics
import sensor

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

filelines = []
listID = []
listTime = []
listHumidity = []
listTemperature = []
listBrightness = []

incoming_currentHumidity = []
incoming_currentTemperature = []
incoming_currentKlux = []

incoming_MaxHumidity = []
incoming_MaxTemperature = []
incoming_MaxLLightlevel = []

incoming_MinHumidity = []
incoming_MinTemperature = []
incoming_MinLLightlevel = []

incoming_averageHumidity = []
incoming_averageTemperature = []
incoming_averageLLightlevel = []

def current_time():
    rightNow = datetime.now()
    time = rightNow.strftime("%d %B %Y, %H:%M:%S")
    time = time.lstrip('0')
    time = time.lower()
    day = rightNow.strftime("%A")

    return "It is " + time + " on a " + day + "."

def current_humidity():
    humidity = sensor.humidity 
    return humidity

def current_temperature():
    temperature = sensor.temperature
    return temperature

def current_klux():
    klux = sensor.klux
    return klux

def calc_average_humidity():
    average_humidity = statistics.mean(recorded_humidities)
    return average_humidity

def calc_average_temperature():
    average_temperatures = statistics.mean(recorded_temperatures)
    return average_temperatures

def calc_average_klux():
    average_klux = statistics.mean(recorded_klux)
    return average_klux

def calc_min_humidites():
    minimal_humidites = min(recorded_humidities)
    return minimal_humidites

def calc_min_temperatures():
    minimal_temperatures = min(recorded_temperatures)
    return minimal_temperatures

def calc_min_klux():
    minimal_klux = min(recorded_klux)
    return minimal_klux

def calc_max_humidity():
    max_humidites = max(recorded_humidities)
    return max_humidites

def calc_max_temperatures():
    max_temperatures = max(recorded_temperatures)
    return max_temperatures

def calc_max_klux():
    max_klux = max(recorded_klux)
    return max_klux

app = Flask(__name__)

@app.route("/")
def homepage():

    recorded_humidities.append(current_humidity())
    recorded_temperatures.append(current_temperature())
    recorded_klux.append(current_klux())

    return render_template('index.html',
                            #current info
                            time = current_time(),
                            humidity = current_humidity(),
                            temperature = current_temperature(),
                            klux = current_klux(),
                            #on average info
                            average_klux = calc_average_klux(),
                            average_temperature = calc_average_temperature(),
                            average_humidity = calc_average_humidity(),
                            #lowest values recorded
                            min_klux = calc_min_klux(),
                            min_temperature = calc_min_temperatures(),
                            min_humidity = calc_min_humidites(),
                            #highest values recorded
                            max_klux = calc_max_klux(),
                            max_temperature = calc_max_temperatures(),
                            max_humidity = calc_max_humidity())

#display csv
@app.route('/show_csv_list', methods=['GET'])
def show_csv_html():

    return render_template('receiveCSV.html',
                            rawLines = len(filelines),
                            sensor_id = listID,
                            time_stamp = listTime,
                            humidity = listHumidity,
                            temperature = listTemperature,
                            brightness = listBrightness)

#receive csv
@app.route("/post_data", methods=["POST"]) 
def receive_data():
    json_data = request.get_json()

    for row in json_data['allRows']:
        filelines.append(row)
    
    for sensorID in json_data['listID']:
        listID.append(sensorID)

    for time in json_data['listTime']:
        listTime.append(time)

    for humidity in json_data['listHumidity']:
        listHumidity.append(humidity)

    for temperature in json_data['listTemperature']:
        listTemperature.append(temperature)

    for brightness in json_data['listBrightness']:
        listBrightness.append(brightness)

    return "OK", 200

#MESSAGE TO TEACHER
#So I made this list since I can't change a variable directly when receiving a json data
#Nor can I do so with getters and setters
#so I took use of the fact that append pushes a variable to the end of the list
#And used [int] values since that is the most recent one
#Sloppy but I couldn't think of anything else so I would hope that you could help me with it


#receive other arduino
@app.route("/post_arduino", methods=["POST"]) 
def receive_arduino():
    json_data = request.get_json()

    incoming_currentHumidity.append(json_data['current_humidity'])
    incoming_currentTemperature.append(json_data['current_temperature'])
    incoming_currentKlux.append(json_data['current_lightlevel'])

    incoming_MaxHumidity.append(json_data['max_humidity'])
    incoming_MaxTemperature.append(json_data['max_temperature'])
    incoming_MaxLLightlevel.append(json_data['max_lightlevel'])

    incoming_MinHumidity.append(json_data['min_humidity'])
    incoming_MinTemperature.append(json_data['min_temperature'])
    incoming_MinLLightlevel.append(json_data['min_lightlevel'])

    incoming_averageHumidity.append(json_data['average_humidity'])
    incoming_averageTemperature.append(json_data['average_temperature'])
    incoming_averageLLightlevel.append(json_data['average_lightlevel'])

    return "OK", 200

#display other arduino
@app.route('/show_arduino_list', methods=['GET'])
def show_arduino_html():

    return render_template('receiveArduino.html',
                            #current info
                            Rtime = current_time(),
                            Rhumidity = incoming_currentHumidity[len(incoming_currentHumidity) - 1],
                            Rtemperature = incoming_currentTemperature[len(incoming_currentTemperature) - 1],
                            Rklux = incoming_currentKlux[len(incoming_currentKlux) - 1],
                            #on average info
                            Raverage_klux = incoming_averageLLightlevel[len(incoming_averageLLightlevel) - 1],
                            Raverage_temperature = incoming_averageTemperature[len(incoming_averageTemperature) - 1],
                            Raverage_humidity = incoming_averageHumidity[len(incoming_averageHumidity) - 1],
                            #lowest values recorded
                            Rmin_klux = incoming_MinLLightlevel[len(incoming_MinLLightlevel) - 1],
                            Rmin_temperature = incoming_MinTemperature[len(incoming_MinTemperature) - 1],
                            Rmin_humidity = incoming_MinHumidity[len(incoming_MinHumidity) - 1],
                            #highest values recorded
                            Rmax_klux = incoming_MaxLLightlevel[len(incoming_MaxLLightlevel) - 1],
                            Rmax_temperature = incoming_MaxTemperature[len(incoming_MaxTemperature) - 1],
                            Rmax_humidity = incoming_MaxHumidity[len(incoming_MaxHumidity) - 1],
                            time = current_time(),
                            humidity = current_humidity(),
                            temperature = current_temperature(),
                            klux = current_klux(),
                            #on average info
                            average_klux = calc_average_klux(),
                            average_temperature = calc_average_temperature(),
                            average_humidity = calc_average_humidity(),
                            #lowest values recorded
                            min_klux = calc_min_klux(),
                            min_temperature = calc_min_temperatures(),
                            min_humidity = calc_min_humidites(),
                            #highest values recorded
                            max_klux = calc_max_klux(),
                            max_temperature = calc_max_temperatures(),
                            max_humidity = calc_max_humidity())
                            