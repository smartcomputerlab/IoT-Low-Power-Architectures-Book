from machine import Pin, I2C, SPI
import machine,ustruct, time, urequests, ubinascii
from lora_init import *
from sensors_display import *
from aes_tools import *
from wifi_tools import *
SSID = 'Bbox-9ECEBF79'
PASSWORD = '54347A3EA6A1D6C36EF6A9E5156F7D'
from umqtt.simple import MQTTClient
# MQTT broker details
MQTT_BROKER = "broker.emqx.io"  # Replace with your broker address
MQTT_PORT = 1883
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Unique client ID
MQTT_TOPIC = 'control/urgent_data'  # Replace with your topic
# Initialize MQTT client
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

lora_modem = lora_init()

wkey=""; rssi=0; chan=0; wkey=""; lumi=0.0; temp=0.0; humi=0.0; data=0

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
    
def publish_sensor_data(lumi, temp, vbat ):
    """Publish sensor data to MQTT broker."""
    if lumi is not None and temp is not None and humi is not None:
        message = {
            "lumi": lumi,
            "temp": temp,
            "humi": vbat
        }
        client.publish(MQTT_TOPIC, str(message))
        print("Published:", message)
    else:
        print("Failed to publish sensor data.")

# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi, rssi):
    global wkey
    try:
        swkey=wkey.decode('utf-8')
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi); sf4="&field4="+str(rssi)
        #url = "https://api.thingspeak.com/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3+sf4
        url = "https://api.thingspeak.com/update?key="+swkey+sf1+sf2+sf3+sf4
        print(url)
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi, rssi)
    except Exception as e:
        print("Failed to send data:", e)
        
    
ack_num=0   
# --- Receive LoRa Packet ---
def onReceive(lora_modem,enc_payload):
    global wkey; global rssi; global lumi; global temp; global humi; global data; global ack_num
    if len(enc_payload)==32:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(8,9,lumi,temp,humi,0)
        ack_num=ack_num+1; print("ack:",ack_num)
        cntr=0; c_def=1; c_max=64; d_min=0.01;d_max=0.2;t_low=16.0; t_high=26.0
        ack=ustruct.pack("4i4f",chan,cntr,c_def,c_max,d_min,d_max,t_low,t_high) 
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora_modem.println(enc_ack)  # sending ACK packet
        print("send long encrypted ack AES packet")
        data=1
        if connect_WiFi(SSID, PASSWORD):
            print("WiFi connected")
            send_data_to_thingspeak(lumi, temp, humi, rssi)
            time.sleep(1); 
            disconnect_WiFi(); time.sleep(15)
            
    elif len(enc_payload)==16:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, lumi, temp, vbat = ustruct.unpack('i3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,lumi,temp,vbat)
        sensors_display(8,9,lumi,temp,vbat,0)
        ack_num=ack_num+1; print("ack:",ack_num)
        cntr=0; c_def=1; c_max=64; d_min=0.01;d_max=0.2;t_low=16.0; t_high=26.0
        ack=ustruct.pack("4i4f",chan,cntr,c_def,c_max,d_min,d_max,t_low,t_high) 
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora_modem.println(enc_ack)  # sending ACK packet
        print("send long encrypted ack AES packet")
        data=1
        if connect_WiFi(SSID, PASSWORD):
            print("WiFi connected")
            connect_mqtt()
            publish_sensor_data(lumi, temp, vbat)
            disconnect_mqtt()
            time.sleep(4) 
            disconnect_WiFi()
            
    lora_modem.receive()

def main():
    global wkey; global rssi; global lumi; global temp; global humi; global data
    ts_wait=10*1500; lastnow=0
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)

main()

