import network , socket , time
from machine import UART

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to WiFi network: {ssid}")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
            print("Waiting for connection...")
    print("Connected to WiFi")
    print("Network Config:", wlan.ifconfig())
    return wlan

def send_UDP_datagram(ip, port, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (ip, port))
        print(f"Message sent to {ip}:{port}")

    except Exception as e:
        print("Error:", e)
    
    finally:
        sock.close()

WIFI_SSID = "Livebox-08B0"
WIFI_PASSWORD = "G79ji6dtEptVTPWmZP"
DEST_IP = "192.168.1.31"  # Example destination IP
DEST_PORT = 8888
# UART Configuration
UART_BAUDRATE = 9600
uart = UART(1, baudrate=UART_BAUDRATE, tx=16, rx=17)
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)
print("Ready to receive UART messages and send datagram...")
while True:
    if uart.any():
        time.sleep(0.1)# necessary to synchronize the UART input buffer
        message = uart.readline().decode('utf-8').strip()
        if message:
            print(f"Received from UART: {message}")
            send_UDP_datagram(DEST_IP,DEST_PORT,message)
            