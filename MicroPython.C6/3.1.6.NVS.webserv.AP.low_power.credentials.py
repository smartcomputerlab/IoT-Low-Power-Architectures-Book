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

def save_power_credentials(key,cycle, delta, kpack):
    """Stores power control parameters: cycle, delta, kpack in ESP32 NVS memory"""
    nvs = esp32.NVS("cycle")
    nvs.set_blob(key,cycle.encode('utf-8'))
    nvs.commit()
    nvs = esp32.NVS("delta")
    nvs.set_blob(key,delta.encode('utf-8'))
    nvs.commit()
    nvs = esp32.NVS("kpack")
    nvs.set_blob(key,kpack.encode('utf-8'))
    nvs.commit()

def get_power_credentials(key):
    """Retrieves MQTT server and topic from NVS storage"""
    try:
        bcycle = bytearray(12);bdelta = bytearray(24);bkpack = bytearray(24)
        nvs = esp32.NVS("cycle")
        cycle=nvs.get_blob(key,bcycle)
        nvs = esp32.NVS("delta")
        delta=nvs.get_blob(key,bdelta)
        nvs = esp32.NVS("kpack")
        kpack=nvs.get_blob(key,bkpack)
    except:
        cycle, delta, kpack = "Not Set", "Not Set", "Not Set"
    return bcycle.decode('ascii'), bdelta.decode('ascii'), bkpack.decode('ascii')

# Load stored WiFi credentials
stored_cycle, stored_delta, stored_kpack = get_power_credentials(key)
print(stored_cycle);print(stored_delta);print(stored_kpack)

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
        <h1>Low Power Control Setup</h1>
        <div class="container">
            <h3>Current Stored Credentials:</h3>
            <p><strong>cycle:</strong> {stored_cycle}</p>
            <p><strong>delta:</strong> {stored_delta}</p>
            <p><strong>kpack:</strong> {stored_kpack}</p>
            <h3>Enter New Power Control Credentials:</h3>
            <form action="/" method="GET">
                <input type="text" name="cycle" placeholder="Enter cycle" required>
                <input type="text" name="delta" placeholder="Enter delta" required>
                <input type="text" name="kpack" placeholder="Enter kpack" required>
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
    if "GET /?cycle=" in request and "&delta=" in request and "&kpack=" in request:
        try:
            cycle_start = request.find("cycle=") + 6
            cycle_end = request.find("&", cycle_start)
            delta_start = request.find("delta=") + 6
            delta_end = request.find("&", delta_start)
            kpack_start = request.find("kpack=") + 6
            kpack_end = request.find(" ", kpack_start)
            new_cycle = request[cycle_start:cycle_end]
            new_delta = request[delta_start:delta_end]
            new_kpack = request[kpack_start:kpack_end]
            # Save new credentials in NVS
            save_power_credentials(key,new_cycle, new_delta, new_kpack)
            print(f"New Power Credentials Saved - cycle: {new_cycle}, delta: {new_delta}, kpack: {new_kpack} ")
            # Reload stored credentials
            stored_cycle, stored_delta, stored_kpack = get_power_credentials(key)
        except Exception as e:
            print("Error processing request:", e)

    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()
    