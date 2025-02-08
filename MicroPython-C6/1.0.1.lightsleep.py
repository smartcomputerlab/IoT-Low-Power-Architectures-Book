import machine
from machine import Pin
import time
led=Pin(15,Pin.OUT)
print("start with lightsleep loop")
c=0

while True:
    led.value(1)
    print("Entering high_power stage")
    print(c); c=c+1
    time.sleep(1)
    print("Entering light sleep...")
    time.sleep(1); led.value(0)
    machine.lightsleep(5000)  # Sleep for 5 seconds
    time.sleep(1)
    print("Woke up from light sleep!")
