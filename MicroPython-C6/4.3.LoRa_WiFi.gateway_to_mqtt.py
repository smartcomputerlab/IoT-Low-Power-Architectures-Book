from machine import Pin, I2C, SPI
from wifi_tools import *
import ustruct, time, random
from lora_init import *
from sensor_display import *
from aes_tools import *
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = "rt_gateway"  # Unique client ID
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic

# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

lora_modem = lora_init()

# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

chan=1234; wkey="smartcomputerlab"; temp=20.0; humi=50.0; lumi=100.0; pack=0

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

def onReceive(lora_modem,payload):
    global chan; global wkey; global temp; global humi; global lumi; global pack
    if len(payload)==32:
        pack=1
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,16)
        ack=ustruct.pack('2ifi',1234,cycle,0.1,10)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(temp,humi,lumi,rssi,0)
    
    lora_modem.receive()

def main():
    global pack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        print("in the loop")
        if pack==1 :
            connect_WiFi(SSID,PASS)
            publish_sensor_data(wkey, lumi, temp, humi)
            time.sleep(1)
            pack = 0
            
        time.sleep(4)
        
main()
