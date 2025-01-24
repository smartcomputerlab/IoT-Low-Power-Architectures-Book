from machine import Pin, deepsleep
import time
# Initialize the LED pin
led = Pin(15, Pin.OUT)
# Turn on the LED
led.value(1)
print("LED is ON")
time.sleep(3)  # Keep the LED on for 5 seconds
# Turn off the LED
led.value(0)
print("LED is OFF")
# Go to deep sleep for 10 seconds
print("Going to sleep for 10 seconds...")
time.sleep(0.5)  # Small delay to ensure the message is printed before sleep
#deepsleep(6000)  # 6 seconds in milliseconds
