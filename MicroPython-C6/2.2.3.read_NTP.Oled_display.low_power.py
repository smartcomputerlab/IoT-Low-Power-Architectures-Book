import time, ntptime, machine
from wifi_tools import connect, disconnect
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
# I2C pins for the OLED display
SDA_PIN = 19
SCL_PIN = 20
# Initialize RTC
rtc = machine.RTC()

# Retrieve cycle counter from RTC memory
rtc_mem = rtc.memory()
if len(rtc_mem) == 0:
    cycle = 0
else:
    cycle = int(rtc_mem.decode())

if cycle == 0:
    # First cycle: Connect to WiFi and sync time
    SSID = "YourNetworkSSID"
    PASSWORD = "YourNetworkPassword"
    
    if connect(SSID, PASSWORD):
        try:
            ntptime.settime()
            print("Time synchronized with NTP server.")
        except OSError as e:
            print("Failed to synchronize time:", e)
        disconnect()
        print("Disconnected from WiFi.")
    else:
        print("Failed to connect to WiFi:", SSID)
        # Continue anyway; the time may not be correct without NTP sync
else:
    # Subsequent cycles: Do not connect to WiFi or re-sync time
    print("No WiFi connection this cycle. Using previously set RTC time.")

# Read current time from RTC
current_time = time.localtime()
hour = current_time[3]
minute = current_time[4]
second = current_time[5]

print("Current UTC Time: {:02d}:{:02d}:{:02d}".format(hour, minute, second))
# Initialize the OLED display
# Adjust frequency and dimensions as per your display specs
i2c = I2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
# Display the current time
oled.fill(0)
oled.text("Time (UTC):", 0, 0)
oled.text("{:02d}:{:02d}:{:02d}".format(hour, minute, second), 0, 16)
oled.show()

# Keep the display on for 3 seconds
time.sleep(3)
# Power off the display
oled.poweroff()
print("Display powered off.")

# Increment cycle counter and store in RTC memory
cycle += 1
rtc.memory(str(cycle).encode())

# Deep sleep for 6 seconds
print("Entering deep sleep for 6 seconds...")
time.sleep_ms(1000)  # small delay before sleep
machine.deepsleep(6*1000)

