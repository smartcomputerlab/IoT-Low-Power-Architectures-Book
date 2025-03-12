import network
import socket
from machine import Pin

# WiFi AP Configuration
SSID = "ESP32AP"
PASSWORD = "smartcomputerlab"

# Initialize and start WiFi in Access Point mode
ap = network.WLAN(network.AP_IF)  # Set ESP32 as an access point
ap.active(True)
ap.config(essid=SSID, password=PASSWORD)  # Set SSID and Password

# Wait until the AP is active
while not ap.active():
    pass

print("AP Active. IP Address:", ap.ifconfig()[0])

# Initialize LED on GPIO 15
led = Pin(15, Pin.OUT)
led.value(0)  # Start with LED OFF

# HTML Web Page
def web_page():
    led_state = "ON" if led.value() else "OFF"
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 LED Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; text-align: center; background-color: #f8f9fa; }}
            h1 {{ color: #007bff; }}
            .button {{ font-size: 20px; padding: 10px; margin: 10px; width: 150px; }}
            .on {{ background-color: green; color: white; }}
            .off {{ background-color: red; color: white; }}
        </style>
    </head>
    <body>
        <h1>ESP32 LED Control</h1>
        <p>LED State: <strong>{led_state}</strong></p>
        <a href="/?led=on"><button class="button on">TURN ON</button></a>
        <a href="/?led=off"><button class="button off">TURN OFF</button></a>
    </body>
    </html>
    """
    return html

# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("Web server is running...")
while True:
    conn, addr = s.accept()
    print("New connection from", addr)
    request = conn.recv(1024).decode()
    
    if "GET /?led=on" in request:
        print("Turning LED ON")
        led.value(1)
    elif "GET /?led=off" in request:
        print("Turning LED OFF")
        led.value(0)

    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    