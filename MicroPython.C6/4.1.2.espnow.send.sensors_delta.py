import network, machine
from machine import Pin, lightsleep, deepsleep
import espnow
import utime, ustruct
from sensors_bat import *
delta=0.06
rtc = machine.RTC()

def read_stemp():
    data = rtc.memory()
    if not data:
        stemp = 20.0
    else:
        stemp = float(data)
    return stemp

def write_stemp(stemp):
    rtc.memory(str(stemp).encode())

led = Pin(15, Pin.OUT)

while True:
    led.value(1)
    lumi,temp,humi,bat=sensors_bat(sda=19,scl=20)
    stemp=read_stemp()
    print(temp,stemp)
    if(abs(temp-stemp)>delta):
        sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
        sta.active(True)
        sta.config(channel=11) # must be provide from gateway channel
        esp = espnow.ESPNow()
        esp.active(True)
        print("now active")
        peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Replace with broadcast MAC address
        esp.add_peer(peer)
        data=ustruct.pack('i16s7f',1254,'YOX31M0EDKO0JATK',bat,lumi,temp,humi,0.0,0.0,0.0)
        write_stemp(temp)
        esp.send(peer, data)
        print("data sent")
        utime.sleep(2)
        led.value(0)
        
    deepsleep(6*1000)
    