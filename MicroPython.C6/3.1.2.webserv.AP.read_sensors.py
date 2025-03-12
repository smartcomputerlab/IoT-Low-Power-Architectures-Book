import network
import socket
import time
from machine import Pin, I2C
from sensors import *

# WiFi AP Configuration
AP_SSID = "ESP32-Sensors"
AP_PASSWORD = "12345678"

# Initialize WiFi in Access Point mode
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

# Wait for AP to activate
while not ap.active():
    pass

print("AP Active. IP Address:", ap.ifconfig()[0])
# HTML Web Page
def web_page():
    
    luminosity,temperature, humidity  = sensors(scl=20,sda=19)
    print(luminosity,temperature, humidity)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Sensor Data</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; text-align: center; background-color: #f8f9fa; }}
            h1 {{ color: #007bff; }}
            .container {{ width: 300px; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 0px 10px gray; }}
            .data-box {{ padding: 10px; margin: 10px; font-size: 20px; background: #f1f1f1; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <h1>ESP32 Sensor Readings</h1>
        <div class="container">
            <h3>Sensor Values:</h3>
            <p class="data-box"><strong>Temperature:</strong> {temperature} C</p>
            <p class="data-box"><strong>Humidity:</strong> {humidity} %</p>
            <p class="data-box"><strong>Luminosity:</strong> {luminosity} Lux</p>
        </div>
    </body>
    </html>
    """
# Start Web Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("Web server is running...")

while True:
    conn, addr = s.accept()
    print("New connection from", addr)
    request = conn.recv(1024).decode()
    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    