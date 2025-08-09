import time
import ntptime
from wifi_tools import *
# Replace with your Wi-Fi credentials
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
# Connect to WiFi
if connect_WiFi(SSID, PASSWORD):
    print("Connected to WiFi:", SSID)
else:
    print("Failed to connect to WiFi:", SSID)
    # If cannot connect to WiFi, can't access NTP. Stop here.
    while True:
        pass
# Synchronize time with NTP server once
try:
    ntptime.settime()
    print("Time synchronized with NTP server.")
except OSError as e:
    print("Failed to synchronize time:", e)

# Now enter an infinite loop where we print the current time every 10 seconds
while True:
    current_time = time.localtime()
    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]
    print("Current UTC Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
    # Wait 10 seconds before the next print
    time.sleep(10)
    
