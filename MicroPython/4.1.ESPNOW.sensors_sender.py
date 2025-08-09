import network
from machine import Pin, deepsleep
import espnow
import utime, ustruct
from sensors import *
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
#sta.disconnect()
sta.active(True)
sta.config(txpower=5.0)
sta.config(channel=1) # must be provide from gateway channel
sta.disconnect()      # For ESP8266
# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)
print("now active")
#peer= b'\x54\x32\x04\x0B\x3C\xF8'  # Replace with receiver's MAC address
peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  #  broadcast MAC address
esp.add_peer(peer)
lumi,temp,humi=sensors(sda=8,scl=9)
print(lumi,temp,humi)
data=ustruct.pack('i16s3f',1254,'YOX31M0EDKO0JATK',lumi,temp,humi)
print(str(data))
esp.send(peer,data)
time.sleep(2)
deepsleep(6*1000)

