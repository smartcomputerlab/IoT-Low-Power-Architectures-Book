from machine import Pin
from time import sleep
led = Pin(3, Pin.OUT)    # connect LED diode to the DevKit: SIG is Pi.OUT
# Blink the LED
while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

