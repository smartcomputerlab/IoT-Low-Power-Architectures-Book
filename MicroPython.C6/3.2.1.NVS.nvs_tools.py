import esp32
key = "credentials"  # Key for the data
# Create NVS storage for SSID & Password
nvs_wifi = esp32.NVS("wifi_config")

def save_credentials(ssid, password):
    nvs_wifi = esp32.NVS("ssid")
    nvs_wifi.set_blob(key,ssid.encode('utf-8'))
    nvs_wifi.commit()
    nvs_wifi = esp32.NVS("password")
    nvs_wifi.set_blob(key,password.encode('utf-8'))
    nvs_wifi.commit()

def get_credentials():
    try:
        bssid = bytearray(18);bpassword = bytearray(18);
        nvs_wifi = esp32.NVS("ssid")
        ssid=nvs_wifi.get_blob(key,bssid)
        nvs_wifi = esp32.NVS("password")
        password=nvs_wifi.get_blob(key,bpassword)
    except:
        ssid, password = "Not Set", "Not Set"
    return bssid.decode('ascii'), bpassword.decode('ascii')

# Create NVS storage for channel & wkey
nvs_ts = esp32.NVS("ts_config")

def save_tspar(channel, wkey):
    nvs_ts = esp32.NVS("channel")
    nvs_ts.set_blob(key,str(channel).encode('utf-8'))
    nvs_ts.commit()
    nvs_ts = esp32.NVS("wkey")
    nvs_ts.set_blob(key,wkey.encode('utf-8'))
    nvs_ts.commit()

def get_tspar():
    try:
        bchannel = bytearray(18);bwkey = bytearray(18);
        nvs_ts = esp32.NVS("channel")
        ssid=nvs_ts.get_blob(key,bchannel)
        nvs_ts = esp32.NVS("wkey")
        password=nvs_ts.get_blob(key,bwkey)
    except:
        channel, wkey = "Not Set", "Not Set"
    return bchannel.decode('ascii'), bwkey.decode('ascii')

def save_mqtt_credentials(key,server, topic):
    """Stores MQTT server and topic in ESP32 NVS memory"""
    nvs = esp32.NVS("server")
    nvs.set_blob(key,server.encode('utf-8'))
    nvs.commit()
    nvs = esp32.NVS("topic")
    nvs.set_blob(key,topic.encode('utf-8'))
    nvs.commit()
    
def get_mqtt_credentials():
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

def get_power_credentials():
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
