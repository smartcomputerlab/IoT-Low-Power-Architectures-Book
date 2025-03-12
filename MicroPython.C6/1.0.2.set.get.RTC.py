import machine
import utime
# Initialize the RTC
rtc = machine.RTC()
# Function to set the RTC time
def set_rtc_time(year, month, day, weekday, hour, minute, second, microsecond=0):
    rtc.datetime((year, month, day, weekday, hour, minute, second, microsecond))
    print("RTC time set to:", rtc.datetime())
# Function to get the RTC time
def get_rtc_time():
    return rtc.datetime()
# Example: Set RTC to 2025-02-13, Thursday, 12:34:56
set_rtc_time(2025, 2, 13, 3, 12, 34, 56)

# Wait a bit
utime.sleep(2)

# Get RTC time
current_time = get_rtc_time()
print("Current RTC Time:", current_time)
