from machine import Pin, I2C, SPI
from wifi_tools import *
import ustruct, urequests
from lora_init import *
from sensor_display import *
import time
from aes_tools import *
import random
from umqtt.simple import MQTTClient
# SSID = 'PhoneAP'
# PASS = 'smartcomputerlab'
SSID = 'Livebox-08B0'
PASS = 'G79ji6dtEptVTPWmZP'

# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

# Initialize LoRa modem
lora_modem = lora_init()

chan=0; wkey=""; temp=20.0; humi=50.0; lumi=100.0; pack=0

 # Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey,lumi,temp,humi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        #url = "http://2.12.92.92:443/update?key=HEU64K3PGNWG36C4"+sf1+sf2+sf3
        url = "https://api.thingspeak.com/update?key="+wkey+sf1+sf2+sf3
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
        pack=1
    except Exception as e:
        print("Failed to send data:", e)

# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    global chan; global wkey; global temp; global humi; global lumi; global pack
    if len(payload)==32:
        pack=1
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,16)
        ack=ustruct.pack('2ifi',chan,cycle,0.1,6)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(8,9,temp,humi,lumi,rssi)
    
    lora_modem.receive()

def main():
    global pack; global wkey; global temp; global humi; global lumi; global pack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        print("in the loop")
        if pack==1 :
            if connect_WiFi(SSID,PASS):
                print("connected")
            print(wkey)
            send_data_to_thingspeak(wkey.decode('utf-8'),lumi,temp,humi)
            time.sleep(1)
            #disconnect()
            pack = 0
            
        time.sleep(4)
        
main()