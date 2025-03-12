from sensors_display import *
from sensors import *
import time
from machine import Pin, lightsleep, deepsleep
led = Pin(15, Pin.OUT)
while True:
    lumi,temp,humi=sensors(scl=20,sda=19)            # connected to high_power I2C
    led.value(1)
    sensors_display(6, 7, lumi, temp, humi,6)        # connected to low_power I2C
    led.value(0)
    #time.sleep(6)
    #lightsleep(6*1000)
    deepsleep(6*1000)
    
    