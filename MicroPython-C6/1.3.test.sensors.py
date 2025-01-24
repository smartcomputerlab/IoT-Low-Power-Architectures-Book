from sensors import *          # all including sensors()
import time
from machine import deepsleep, Pin

led = Pin(15, Pin.OUT)
# Turn off the LED
led.value(0)

# Assume the I2C bus is on GPIO 21 (SDA) and GPIO 22 (SCL) for ESP32C6 - BF2
while True:
    lumi, temp, humi = sensors(sda=19, scl=20)
    print("Luminosity:", lumi, "lux")
    print("Temperature:", temp, "C")
    print("Humidity:", humi, "%")
    time.sleep(5)
    #deepsleep(10)
    