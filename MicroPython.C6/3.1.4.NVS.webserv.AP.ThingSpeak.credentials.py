import network
import socket
import esp32

# WiFi AP Configuration
AP_SSID = "ESP32-ThingSpeak"
AP_PASSWORD = "12345678"

# Initialize WiFi as Access Point
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

# Wait until the AP is active
while not ap.active():
    pass

print("AP Active. IP Address:", ap.ifconfig()[0])

# Create NVS storage for ThingSpeak parameters
# Create NVS storage for channel & wkey
key = "credentials"  # Key for the data
nvs_ts = esp32.NVS("ts_config")

def save_thingspeak_credentials(channel, wkey):
    nvs_ts = esp32.NVS("channel")
    nvs_ts.set_blob(key,str(channel).encode('utf-8'))
    nvs_ts.commit()
    nvs_ts = esp32.NVS("wkey")
    nvs_ts.set_blob(key,wkey.encode('utf-8'))
    nvs_ts.commit()
    
    
def get_thingspeak_credentials():
    try:
        bchannel = bytearray(18);bwkey = bytearray(18);
        nvs_ts = esp32.NVS("channel")
        ssid=nvs_ts.get_blob(key,bchannel)
        nvs_ts = esp32.NVS("wkey")
        password=nvs_ts.get_blob(key,bwkey)
    except:
        channel, wkey = "Not Set", "Not Set"
    return bchannel.decode('ascii'), bwkey.decode('ascii')

# Load stored ThingSpeak credentials
stored_channel, stored_write_key = get_thingspeak_credentials()
# HTML Web Page
def web_page():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 ThingSpeak Setup</title>
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
        <h1>ThingSpeak Setup</h1>
        <div class="container">
            <h3>Stored ThingSpeak Credentials:</h3>
            <p><strong>Channel Number:</strong> {stored_channel}</p>
            <p><strong>Write Key:</strong> {stored_write_key}</p>
            <h3>Enter New Credentials:</h3>
            <form action="/" method="GET">
                <input type="number" name="channel" placeholder="Enter Channel Number" required>
                <input type="text" name="write_key" placeholder="Enter Write API Key" required>
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
    
    # Check if ThingSpeak data was submitted
    if "GET /?channel=" in request and "&write_key=" in request:
        try:
            channel_start = request.find("channel=") + 8
            channel_end = request.find("&", channel_start)
            write_key_start = request.find("write_key=") + 10
            write_key_end = request.find(" ", write_key_start)

            new_channel = request[channel_start:channel_end]
            new_write_key = request[write_key_start:write_key_end]

            # Save new credentials in NVS
            save_thingspeak_credentials(new_channel, new_write_key)
            print(f"New ThingSpeak Credentials Saved - Channel: {new_channel}, Write Key: {new_write_key}")

            # Reload stored credentials
            stored_channel, stored_write_key = get_thingspeak_credentials()
        except Exception as e:
            print("Error processing request:", e)

    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    
