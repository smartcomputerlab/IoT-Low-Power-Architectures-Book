from machine import Pin, I2C, SPI
from wifi_tools import *
import ustruct, urequests
from lora_init import *
from sensor_display import *
import time, ustruct
from aes_tools import *
import random
from umqtt.simple import MQTTClient
    
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

# Initialize LoRa modem
lora_modem = lora_init()

start=0

chan=1234; wkey="smartcomputerlab"; temp=20.0; humi=50.0; lumi=100.0; pack=0
cycle=10; delta=0.1; kpack=10

# ThingSpeak API details
THINGSPEAK_CHANNEL_ID = '1626377'          # Replace with your ThingSpeak channel ID
THINGSPEAK_READ_API_KEY = '9JVTP8ZHVTB9G4TT'       # Replace with your ThingSpeak read API key
THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json'

# Function to read data from ThingSpeak
def read_data_from_thingspeak():
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_READ_API_KEY}&results=1"
        response = urequests.get(url)
        data = response.json()
        response.close()
        # Extract the latest feed (last entry)
        feed = data['feeds'][0]
#         created_at=feed.get(“created_at”, “Unknown”)
#         print(f"Last record timestamp: {created_at}")
        cycle = feed['field1']
        delta = feed['field2']
        kpack = feed['field3']
        return int(cycle),float(delta), int(kpack)
    except Exception as e:
        print("Failed to retrieve data:", e)
        return None, None, None

 # Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey,lumi, temp, humi,rssi):
    try:
        sf1="&field1="+str(lumi);sf2="&field2="+str(temp);sf3="&field3="+str(humi);sf4="&field4="+str(rssi)
        #url = "http://2.12.92.92:443/update?key=HEU64K3PGNWG36C4"+sf1+sf2+sf3+sf4
        url = "https://107.23.148.232/update?key="+wkey+sf1+sf2+sf3+sf4
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send data:", e)
    #client.disconnect()

# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    global chan; global wkey; global temp; global humi; global lumi; global start
    global cycle; global delta; global kpack
    if len(payload)==32:
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,16)
        ack=ustruct.pack('2ifi',1234,cycle,delta,kpack)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(temp,humi,lumi,rssi)
        if (time.time() - start) > 20:
            print("time to send")
            send_data_to_thingspeak("YOX31M0EDKO0JATK",lumi, temp, humi,rssi)
            start = time.time()
    
    lora_modem.receive()

def main():
    global cycle; global delta; global kpack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    connect(SSID,PASS)
    time.sleep(0.4)
    while True:
        print("in the loop")
        cycle,delta,kpack=read_data_from_thingspeak()
        print("cycle:"+str(cycle)+" delta:"+str(delta)+" kpack:"+str(kpack))
        time.sleep(12)
        
main()
