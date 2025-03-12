from machine import Pin, lightsleep, deepsleep
import time
# Initialize the LED pin
led = Pin(15, Pin.OUT)
counter=0
while True:
    counter=counter+1
    print(counter)
    led.value(1)
    print("LED is ON")
    time.sleep(6)  # Keep the LED on for 6 seconds
    # Turn off the LED
    led.value(0)
    print("LED is OFF")
    print("Going to sleep for 6 seconds...")
    #time.sleep(6)       # active sleep for 6 seconds
    lightsleep(6*1000)   # lightsleep for 6 seconds
    #deepsleep(6000)      # deepsleep for 6 seconds
    
    