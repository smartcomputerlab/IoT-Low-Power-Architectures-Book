from machine import Pin, deepsleep
import time
# Initialize the SIG pin
led = Pin(3, Pin.OUT)
# Turn on the SIG
led.value(1)
print("SIG is ON")
time.sleep(3)  
# Turn off the LED
led.value(0)
print("SIG is OFF")
time.sleep(3)    
print("Going to sleep for 6 seconds…"); time.sleep(1)
deepsleep(6000)  # 6 seconds in milliseconds

