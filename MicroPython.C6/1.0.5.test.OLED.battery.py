from machine import Pin, ADC
import time
from battery_display import *

led=Pin(15,Pin.OUT)

while True:
    led.value(1)
    bat = ADC(Pin(0))
    bat.atten(ADC.ATTN_11DB)      #Full range: 3.3v
    battery = bat.read()*8.12/4096
    print(f"Battery {battery}")
    battery_display(6,7,battery,5)   # using low_power I2C interface
    led.value(0)
    time.sleep(2)
    