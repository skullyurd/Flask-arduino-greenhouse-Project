import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4

DHTPIN  = 12

humidity = 0
temperature = 0
lightlevel = 0
klux = 0

def Measure(data):
    global humidity, temperature
    if (data[3] == 0):
        humidity = data[4]
        temperature = data[5]
        
def setup():
    global board
    board = CustomPymata4(com_port = "COM5")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.05, callback=Measure)
    board.set_pin_mode_analog_input(2, callback=callback_ldr, differential=50)

def callback_ldr(data):
    global klux
    sensor_value = data[2]
    resistance_sensor = (1023-sensor_value)*10/sensor_value

    klux = 325 * pow(resistance_sensor, -1.4) / 1000
    board.displayShow(klux)

def loop():
    global humidity, temperature, klux
    print(humidity, temperature, klux)
    board.displayShow(klux)
    time.sleep(0.01)

setup()
loop()