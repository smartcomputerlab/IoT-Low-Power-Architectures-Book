from machine import Pin, I2C, SPI
import machine,ustruct, time, ubinascii
from lora_init import *
from sensors_display import *
from aes_tools import *
from wifi_tools import *
from umqtt.simple import MQTTClient
SSID = 'Bbox-9ECEBF79'
PASSWORD = '54347A3EA6A1D6C36EF6A9E5156F7D'
# MQTT broker details
MQTT_BROKER = "broker.emqx.io"  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID
MQTT_TOPIC = 'risc-v/sensor_data'  # Replace with your topic
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
lora_modem = lora_init()

def connect_mqtt():
    """Connect to the MQTT broker."""
    try:
        client.connect()
        print("Connected to MQTT broker.")
    except Exception as e:
        print("Failed to connect to MQTT broker:", e)

def disconnect_mqtt():
    client.disconnect()
    print("Disconnected from MQTT broker.")
    
def publish_sensor_data(lumi, temp, humi ):
    """Publish sensor data to MQTT broker."""
    if lumi is not None and temp is not None and humi is not None:
        message = {
            "lumi": lumi,
            "temp": temp,
            "humi": humi
        }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")
    
# --- Receive LoRa Packet ---
def onReceive(lora_modem,enc_payload):
    if len(enc_payload)==32:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(8,9,lumi,temp,humi,0)
        ack=ustruct.pack('2i2f',chan,10,0.1,32.9)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora_modem.println(enc_ack)  # sending ACK packet
        connect_mqtt()
        publish_sensor_data(lumi, temp, humi)
        disconnect_mqtt()
        lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    if connect_WiFi(SSID,PASSWORD):
        print("WiFi connected")
    while True:
        time.sleep(2)
        print("in the loop")
        
main()

