import socket
from machine import deepsleep
import time
from wifi_tools import *
from sensors import *
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
UDP_IP = "192.168.1.61"  # Replace with the receiver's IP address
UDP_PORT = 8899          # Replace with the desired port
MESSAGE = "Hello, ESP32C3!"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    connect_WiFi(SSID,PASSWORD)
    lumi,temp,humi = sensors(8,9)
    message="Lumi:"+str(lumi)+", Temp:"+str(temp)+" ,Humi:"+str(humi)
    print(f"Sending message:" + message)
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    time.sleep(5)  # Send every 2 seconds
    disconnect_WiFi()
except KeyboardInterrupt:
    time.sleep(2)
    print("UDP sender stopped.")
finally:
    sock.close()
    time.sleep(2)
    print("Going to deepsleep")
    deepsleep(10*1000)
