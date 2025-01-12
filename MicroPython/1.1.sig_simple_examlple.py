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
# Go to deep sleep for 10 seconds
print("Going to sleep for 10 seconds...")
time.sleep(3)  # Small delay to ensure the message is printed before sleep
deepsleep(6000)  # 10 seconds in milliseconds
