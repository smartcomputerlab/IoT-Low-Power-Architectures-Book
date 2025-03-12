# time_display.py
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

def time_display(sda, scl, hour,minute,second, duration):
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
    width = 128
    height = 64
    oled = SSD1306_I2C(width, height, i2c)
    oled.fill(0)
    oled.text("Time", 0, 0)
    oled.text("H: "+str(hour), 0, 16)
    oled.text("M: "+str(minute), 0, 28)
    oled.text("S: "+str(second), 0, 40)
    oled.show()
    if duration:
        time.sleep(duration)
        oled.poweroff()
        
        