import time
from conf import *

# Initialize WiFi in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to WiFi
if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)

# Get and display WiFi channel number
wifi_info = wlan.status('rssi')  # Fetch RSSI (workaround for active connection)
channel_number = wlan.config('channel')  # Get the current WiFi channel

print(f"Connected to {ssid}")
print(f"WiFi Channel: {channel_number}")

# Optional: Display IP details
print("Network Config:", wlan.ifconfig())

mac_address = wlan.config("mac")
print(mac_address)
print("Device MAC Address:", ":".join(["{:02X}".format(byte) for byte in mac_address]))
