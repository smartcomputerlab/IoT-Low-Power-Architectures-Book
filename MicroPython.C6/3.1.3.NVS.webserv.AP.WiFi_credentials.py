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
nvs = esp32.NVS("wifi_config")

def save_credentials(key,ssid, password):
    """Stores SSID and Password in ESP32 NVS memory"""
    nvs = esp32.NVS("ssid")
    nvs.set_blob(key,ssid.encode('utf-8'))
    nvs.commit()
    nvs = esp32.NVS("password")
    nvs.set_blob(key,password.encode('utf-8'))
    nvs.commit()

def get_credentials(key):
    """Retrieves SSID and Password from NVS storage"""
    try:
        bssid = bytearray(18);bpassword = bytearray(18);
        nvs = esp32.NVS("ssid")
        ssid=nvs.get_blob(key,bssid)
        nvs = esp32.NVS("password")
        password=nvs.get_blob(key,bpassword)
    except:
        ssid, password = "Not Set", "Not Set"
    return bssid.decode('ascii'), bpassword.decode('ascii')

# Load stored WiFi credentials
stored_ssid, stored_password = get_credentials(key)
print(stored_password)
print(stored_ssid)

# HTML Web Page
def web_page():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WiFi Setup</title>
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
        <h1>ESP32 WiFi Setup</h1>
        <div class="container">
            <h3>Current Stored Credentials:</h3>
            <p><strong>SSID:</strong> {stored_ssid}</p>
            <p><strong>Password:</strong> {stored_password}</p>
            <h3>Enter New WiFi Credentials:</h3>
            <form action="/" method="GET">
                <input type="text" name="ssid" placeholder="Enter SSID" required>
                <input type="password" name="password" placeholder="Enter Password" required>
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
    if "GET /?ssid=" in request and "&password=" in request:
        try:
            ssid_start = request.find("ssid=") + 5
            ssid_end = request.find("&", ssid_start)
            password_start = request.find("password=") + 9
            password_end = request.find(" ", password_start)
            new_ssid = request[ssid_start:ssid_end]
            new_password = request[password_start:password_end]
            # Save new credentials in NVS
            save_credentials(key,new_ssid, new_password)
            print(f"New Credentials Saved - SSID: {new_ssid}, Password: {new_password}")
            # Reload stored credentials
            stored_ssid, stored_password = get_credentials(key)
        except Exception as e:
            print("Error processing request:", e)

    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    