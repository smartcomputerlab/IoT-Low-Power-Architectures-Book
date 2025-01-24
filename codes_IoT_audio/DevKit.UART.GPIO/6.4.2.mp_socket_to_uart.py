import socket
import machine
import network
import time

# WiFi Configuration
SSID = "Livebox-08B0"         # Replace with your WiFi network name
PASSWORD = "G79ji6dtEptVTPWmZP" # Replace with your WiFi password

# UDP Configuration
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 8888    # Port for UDP communication

# Configure UART
uart = machine.UART(1, baudrate=9600, tx=16, rx=17)  # GPIO: tx=17, rx=16 - USB: tx=16, rx=17
print("UART configured: TX=17, RX=16, Baudrate=9600")

def connect_to_wifi(ssid, password):
    """Connect to WiFi."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("WiFi connected:", wlan.ifconfig())

# Connect to WiFi
connect_to_wifi(SSID, PASSWORD)

# Configure UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print(f"Listening for UDP datagrams on {UDP_IP}:{UDP_PORT}")

# Main loop: Receive UDP data and send to UART
while True:
    try:
        # Receive data from UDP
        data, addr = sock.recvfrom(1024)  # Buffer size 1024 bytes
        print(f"Received from {addr}: {data.decode("utf-8")}")

        # Transmit data over UART
        uart.write(data.decode("utf-8"))
        print("Data transmitted to UART")

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)  # Small delay to avoid rapid retries
        