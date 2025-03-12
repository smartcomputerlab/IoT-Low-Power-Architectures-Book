from machine import Pin, lightsleep, deepsleep, RTC
import time, ustruct
from counter_display import *
# Get the RTC object
rtc = RTC()

# Initialize the LED pin
led = Pin(15, Pin.OUT)
counter=0; val=0
while True:
    # Read the current memory contents
    data = rtc.memory()
    if not data: # If empty, this is the first cycle
        data=ustruct.pack('2i',val,counter)
    else:  
        val,counter = ustruct.unpack('2i', data)
        
    counter+=1; val+=2
    data=ustruct.pack('2i',val,counter)
    rtc.memory(data)
    print(counter)
    led.value(1)
    print("LED is ON")
    counter_display(19,20,val,counter,6)
    # Turn off the LED
    led.value(0)
    print("LED is OFF")
    print("Going to sleep for 6 seconds...")
    #time.sleep(6)        # active sleep for 6 seconds
    #lightsleep(6*1000)   # lightsleep for 6 seconds
    deepsleep(6000)       # deepsleep for 6 seconds
    