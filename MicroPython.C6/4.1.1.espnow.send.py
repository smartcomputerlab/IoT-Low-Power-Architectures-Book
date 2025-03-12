import network
from machine import Pin, deepsleep
import espnow, utime, ustruct
from sensors_bat import *
led = Pin(15, Pin.OUT)
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.config(channel=11) 		# must be provided from AP channel
esp = espnow.ESPNow()
esp.active(True)
print("now active")
#peer= b'\x54\x32\x04\x0B\x3C\xF8'  	# Replace with receiver's MAC address
peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  	# Replace with broadcast MAC address
esp.add_peer(peer)

while True:
    led.value(1)
    lumi,temp,humi,bat=sensors_bat(sda=19,scl=20)
    data=ustruct.pack('i16s7f',1254,'YOX31M0EDKO0JATK',bat,lumi,temp,humi)
    esp.send(peer, data)
    print(data)
    utime.sleep(1)
    led.value(0)
    deepsleep(6*1000)
    