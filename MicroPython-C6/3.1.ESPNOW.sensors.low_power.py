import network
from machine import Pin, deepsleep
import espnow
import utime, ustruct
from sensors import *
led = Pin(15, Pin.OUT)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.config(txpower=8.5)
sta.config(channel=11) # must be provide from gateway channel
sta.disconnect()      # For ESP8266
# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)
print("now active")
peer= b'\x54\x32\x04\x0B\x3C\xF8'  # Replace with receiver's MAC address
#peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Replace with broadcast MAC address
esp.add_peer(peer)

while True:
# Turn on the LED
    led.value(1)
    lumi,temp,humi=sensors(sda=19,scl=20)
    data=ustruct.pack('i16s3f',1254,'YOX31M0EDKO0JATK',lumi,temp,humi)
    esp.send(peer, data)
    utime.sleep(2)
    led.value(0)
    deepsleep(12*1000)
    