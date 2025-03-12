import network
import socket
import esp32
from machine import Pin

# WiFi AP Configuration
AP_SSID = "ESP32AP"
AP_PASSWORD = "smartcomputerlab"
key = "credentials"  # Key for the data

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

# Wait until the AP is active
while not ap.active():
    pass

print("AP Active. IP Address:", ap.ifconfig()[0])
# Create NVS storage for SSID & Password
nvs = esp32.NVS("mqtt_config")

def save_mqtt_credentials(key,server, topic):
    """Stores MQTT server and topic in ESP32 NVS memory"""
    nvs = esp32.NVS("server")
    nvs.set_blob(key,server.encode('utf-8'))
    nvs.commit()
    nvs = esp32.NVS("topic")
    nvs.set_blob(key,topic.encode('utf-8'))
    nvs.commit()

def get_mqtt_credentials(key):
    """Retrieves MQTT server and topic from NVS storage"""
    try:
        bserver = bytearray(24);btopic = bytearray(24)
        nvs = esp32.NVS("server")
        server=nvs.get_blob(key,bserver)
        nvs = esp32.NVS("topic")
        topic=nvs.get_blob(key,btopic)
    except:
        server, topic = "Not Set", "Not Set"
    return bserver.decode('ascii'), btopic.decode('ascii')

# Load stored WiFi credentials
stored_server, stored_topic = get_mqtt_credentials(key)
print(stored_server)
print(stored_topic)


# HTML Web Page
def web_page():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MQTT Setup</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: Arial; text-align: center; background-color: #f8f9fa; }}
            h1 {{ color: #007bff; }}
            .container {{ width: 300px; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0px 0px 10px gray; }}
            input, button {{ width: 90%; padding: 10px; margin: 10px 0; font-size: 18px; }}
            button {{ background-color: #28a745; color: white; border: none; cursor: pointer; }}
            button:hover {{ background-color: #218838; }}
        </style>
    </head>
    <body>
        <h1>ESP32 MQTT Setup</h1>
        <div class="container">
            <h3>Current Stored Credentials:</h3>
            <p><strong>server:</strong> {stored_server}</p>
            <p><strong>topic:</strong> {stored_topic}</p>
            <h3>Enter New MQTT Credentials:</h3>
            <form action="/" method="GET">
                <input type="text" name="server" placeholder="Enter server" required>
                <input type="text" name="topic" placeholder="Enter topic" required>
                <button type="submit">Save</button>
            </form>
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
    
    # Check if SSID and Password were submitted
    if "GET /?server=" in request and "&topic=" in request:
        try:
            server_start = request.find("server=") + 7
            server_end = request.find("&", server_start)
            topic_start = request.find("topic=") + 6
            topic_end = request.find(" ", topic_start)
            new_server = request[server_start:server_end]
            new_topic = request[topic_start:topic_end]
            # Save new credentials in NVS
            save_mqtt_credentials(key,new_server, new_topic)
            print(f"New Credentials Saved - MQTT: {new_server}, topic: {new_topic}")
            # Reload stored credentials
            stored_server, stored_topic = get_mqtt_credentials(key)
        except Exception as e:
            print("Error processing request:", e)

    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    