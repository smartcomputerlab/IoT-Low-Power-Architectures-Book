from sensors import sensors
import time
from machine import deepsleep
while True:
    lumi, temp, humi = sensors(sda=8, scl=9)
    print("Luminosity:", lumi, "lux");print("Temperature:", temp, "C")
    print("Humidity:", humi, "%")
    time.sleep(5)
    #deepsleep(10*1000)  # attention deepsleep needs milliseconds !

