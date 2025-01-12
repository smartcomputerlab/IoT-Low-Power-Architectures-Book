import network
from machine import Pin
import ustruct
import espnow
# Initialize the network interface

def format_mac_address(mac_bytes):
    if len(mac_bytes) != 6:
        raise ValueError("Invalid MAC address length. Expected 6 bytes.")
    return ':'.join(f'{byte:02X}' for byte in mac_bytes)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if wlan.active():
    # Get the MAC address
    mac_address = wlan.config("mac")
    print(mac_address)
    print("Device MAC Address:", ":".join(["{:02X}".format(byte) for byte in mac_address]))
else:
    print("Wi-Fi is not active.")

import network

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(txpower=5.0)
print("Running on channel:", sta.config("channel"))
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow(); e.active(True)

while True:
    host, data = e.recv()
    if data:             # msg == None if timeout in recv()
            chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', data)   # wkey may be topic
            print(format_mac_address(host))
            for_wkey="{:s}".format(wkey)
            print("wkey:"+str(for_wkey)+" lumi:"+str(lumi)+" temp:"+str(temp)+" humi:"+str(humi))
            msg= "lumi:"+str(lumi)+"; temp:"+str(temp)+"; humi:"+str(humi)
            