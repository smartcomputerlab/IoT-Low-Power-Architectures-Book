from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensors_display import *
import time
from aes_tools import *
from wifi_tools import *
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
# MQTT broker details
MQTT_BROKER = 'broker.emqx.io'  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = "rt_gateway"  # Unique client ID
MQTT_TOPIC = 'esp32/sensor_data'  # Replace with your topic
AES_KEY = b'smartcomputerlab'

# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

def publish_sensor_data(topic, temp, humi, lumi):
    if connect_wifi(SSID,PASS):
        print("WiFi connected")
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
 
lora_modem = lora_init()
 
def onReceive(lora_modem,payload):
    rssi = lora_modem.packetRssi()
    decrypted_payload=aes_decrypt(payload,AES_KEY)
    chan, wkey, battery, temp, humi, lumi, s5,s6,s7 = ustruct.unpack('i16s7f', decrypted_payload)
    print("Received LoRa packet:"+str(rssi))   #, payload.decode())
    sensors_display(19,20,temp,humi,lumi,rssi,battery,0)
    chan=123; cycle=10; delta=0.1;kpack=20
    ack=ustruct.pack('2ifi', chan,cycle,delta,kpack)
    encrypted_ack=aes_encrypt(ack,AES_KEY)
    print("sending ACK packet")
    lora_modem.println(encrypted_ack)  # sending ACK packet
    publish_sensor_data(MQTT_TOPIC,temp, humi,lumi)
    lora_modem.receive()
    
    
def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(6)
        print("in the loop")
        
main()
