from machine import Pin, I2C, SPI
from wifi_tools import *
import ustruct
from lora_init import *
from sensor_display import *
import time, ustruct
from aes_tools import *
import random
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = "rt_gateway"  # Unique client ID
MQTT_TOPIC_DATA = 'esp32/sensor_data'  # Replace with your topic
MQTT_TOPIC_CONTROL = 'esp32/control'  # Replace with your topic

# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

# Initialize LoRa modem
lora_modem = lora_init()
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

start=0
chan=1234; wkey="smartcomputerlab"; temp=20.0; humi=50.0; lumi=100.0; pack=0
cycle=10; delta=0.1; kpack=10

# MQTT message callback function
def mqtt_callback(topic, data):
    global cycle; global delta; global kpack
    print("Received message:", data)
    decoded_str = data.decode('utf-8')
    parts = decoded_str.split(',')
    cycle = int(parts[0]); print(cycle)
    delta = float(parts[1]); print(delta)
    kpack = int(parts[2]); print(kpack)

def publish_sensor_data(topic, lumi, temp, humi):
    """Publish sensor data to MQTT broker."""
#     client.connect()
#     time.sleep(1)
    if lumi is not None and temp is not None and humi is not None:
        message = {
            "luminosity": lumi,  "temperature": temp,  "humidity": humi }
        client.publish(topic, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
        
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
        if (time.time() - start) > 20:        # dynamic delay
            print("time to send")
            publish_sensor_data(MQTT_TOPIC_DATA, lumi, temp, humi)
            start = time.time()
            
    lora_modem.receive()

def main():
    global pack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    client.set_callback(mqtt_callback)
    connect(SSID,PASS)
    print("Connected to MQTT broker.")
    client.connect()
    client.subscribe(MQTT_TOPIC_CONTROL)
    print("Subscribed to topic:", MQTT_TOPIC_CONTROL)
    time.sleep(0.4)
    while True:
        print("in the loop")
        client.wait_msg()
        time.sleep(2)

main()
