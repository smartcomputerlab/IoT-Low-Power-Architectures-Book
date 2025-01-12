from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from wifi_tools import *
from sensor_display import *
import time
from aes_tools import *
import random
from umqtt.simple import MQTTClient
# WiFi credentials
# SSID = 'PhoneAP'
# PASS = 'smartcomputerlab'
SSID = 'Livebox-08B0'
PASS = 'G79ji6dtEptVTPWmZP'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = "rt_gateway"  # Unique client ID
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic
# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
# Initialize LoRa modem
lora_modem = lora_init()

# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

wkey=""; lumi=0.0; temp=0.0; humi=0.0

recv=0

def publish_sensor_data(topic, lumi, temp, humi):
    """Publish sensor data to MQTT broker."""
    client.connect()
    time.sleep(1)
    if lumi is not None and temp is not None and humi is not None:
        message = {
            "luminosity": lumi,
            "temperature": temp,
            "humidity": humi
        }
        client.publish(topic, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
        
    client.disconnect()
# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    global wkey; global lumi; global temp; global humi; global recv
    if len(payload)==32:
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,26)
        ack=ustruct.pack('2ifi',chan,cycle,0.01,10)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(8,9,temp,humi,lumi,rssi)
        time.sleep(1)
        recv=1
  
            
    lora_modem.receive()

def main():
    global wkey; global lumi; global temp; global humi
    global recv
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        connect_WiFi(SSID,PASS)
        if recv==1:
            publish_sensor_data(wkey, lumi, temp, humi); recv=0
        # in gateway do not disconnect WiFi ! , just try to connect
main()
