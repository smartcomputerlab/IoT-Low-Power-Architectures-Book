from sensors_display import *
from machine import deepsleep
# Example sensor values
lux = 123.4567
temp = 25.6789
hum = 45.2345
# Call the function with GPIO pin numbers for SDA and SCL
# Adjust SDA, SCL pins according to your board wiring
sensors_display(19, 20, lux, temp, hum,5)
#deepsleep(10*1000)      # go to deepsleep for 10 seconds
