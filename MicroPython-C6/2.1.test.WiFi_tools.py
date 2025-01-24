from wifi_tools import *
import network

# Replace with your own WiFi credentials
SSID = "YourNetworkSSID"
PASSWORD = "YourNetworkPassword"

if connect_wifi(SSID, PASSWORD):
    print("Connected to WiFi:", SSID)
    print("Network config:", network.WLAN(network.STA_IF).ifconfig())
else:
    print("Failed to connect to WiFi:", SSID)

# Scan available networks
networks = scan_wifi()
print("Available networks:")
for net in networks:
    ssid, bssid, channel, RSSI, authmode, hidden = net
    print("SSID:", ssid.decode('utf-8'), "| RSSI:", RSSI)

# Disconnect from current WiFi network
disconnect_wifi()
print("Disconnected from WiFi")

