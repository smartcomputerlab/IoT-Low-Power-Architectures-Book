import socket
import time
from wifi_tools import *
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
UDP_IP = "192.168.1.61"  # Replace with the receiver's IP address
UDP_PORT = 8899          # Replace with the desired port
MESSAGE = "Hello, from RISC-V!"
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    while True:
        if(connect_WiFi(SSID,PASSWORD)):
            print("WiFi connected")
        print(f"Sending message: {MESSAGE}")
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        time.sleep(5)  # Send every 2 seconds
        disconnect_WiFi()
except KeyboardInterrupt:     
    time.sleep(5)          # to allow stop
    print("UDP sender stopped.")
finally:
    sock.close()

