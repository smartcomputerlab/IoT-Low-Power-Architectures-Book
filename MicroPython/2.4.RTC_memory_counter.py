from machine import Pin, I2C, RTC, deepsleep
from ssd1306 import SSD1306_I2C
import time

def display_count(sda, scl, counter, dur):
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    oled.text("RTC Counter", 0, 0)
    oled.text("Count: "+ str(counter), 0, 16)
    oled.show()
    time.sleep(dur)
    oled.poweroff()

# Get the RTC object
rtc = RTC()
# Read the current memory contents
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    # If empty, this is the first cycle
    cycle = 0
else:
    # Convert stored bytes to integer
    cycle = int(rtc_mem.decode())
# Print the current cycle count
print("Current cycle count:", cycle)
# Increment the cycle counter
cycle += 1
display_count(8,9,cycle,3)
# Save the new cycle count to RTC memory
rtc.memory(str(cycle).encode())
print("Going to deep sleep for 10 seconds...")
time.sleep_ms(1000)  # small delay before entering sleep
deepsleep(10*1000)

