
# Initialize the network interface
wlan = network.WLAN(network.STA_IF)
# Activate the WLAN Interface
wlan.active(True)

def format_mac_address(mac_bytes):
    if len(mac_bytes) != 6:
        raise ValueError("Invalid MAC address length. Expected 6 bytes.")
    return ':'.join(f'{byte:02X}' for byte in mac_bytes)

# Check if the interface is active (connected)
if wlan.active():
    # Get the MAC address
    mac_bytes = wlan.config("mac")
    print(mac_bytes)
    print("Device MAC Address:", ":"+format_mac_address(mac_bytes))
else:
    print("Wi-Fi is not active.")

import network
from machine import Pin
import espnow

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(txpower=8.5)
print("Running on channel:", sta.config("channel"))
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(format_mac_address(host), msg)
        
        
        