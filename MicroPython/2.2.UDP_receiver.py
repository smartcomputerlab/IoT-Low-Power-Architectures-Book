import socket
from wifi_tools import *
SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
# Configuration
UDP_IP = "192.168.1.61"  # Listen on all available interfaces
UDP_PORT = 8899     # Port to listen on
# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening for UDP messages on port {UDP_PORT}...")
try:
    connect_WiFi(SSID,PASSWORD)
    while True:
        data, addr = sock.recvfrom(1024)  # Buffer size of 1024 bytes
        print(f"Received message: {data.decode('utf-8')} from {addr}")
except KeyboardInterrupt:
    print("UDP receiver stopped.")
finally:
    sock.close()
    