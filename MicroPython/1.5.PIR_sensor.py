from machine import Pin
import utime
# Define the pin for the PIR sensor
pir_pin = Pin(3, Pin.IN)  # Replace with the GPIO pin connected to the PIR sensor
print("PIR Sensor Test Program")

try:
    while True:
        if pir_pin.value() == 1:
            print("Present")
            
        utime.sleep(0.5)  # Delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program terminated.")

