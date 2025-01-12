import time
import ntptime
import machine
from wifi_tools import *
from machine import Pin, I2C
from display_time import *
rtc = machine.RTC()
# Retrieve cycle counter from RTC memory
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    cycle = 0
else:
    cycle = int(rtc_mem.decode())

if cycle == 0:
    # First cycle: Connect to WiFi and sync time
    SSID = "PhoneAP"
    PASSWORD = "smartcomputerlab"
    connect(SSID, PASSWORD)
    try:
        ntptime.settime()
        print("Time synchronized with NTP server.")
    except OSError as e:
        print("Failed to synchronize time:", e)
    disconnect()

# Read current time from RTC
current_time = time.localtime()
hour = current_time[3]
minute = current_time[4]
second = current_time[5]
print("Current UTC Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
display_time(hour,minute,second,4)
# Increment cycle counter and store in RTC memory
cycle += 1
rtc.memory(str(cycle).encode())
# Deep sleep for 6 seconds
print("Entering deep sleep for 6 seconds...")
time.sleep_ms(100)  # small delay before sleep
machine.deepsleep(6000)
