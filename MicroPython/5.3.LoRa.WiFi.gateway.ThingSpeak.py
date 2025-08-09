from machine import Pin, I2C, SPI
import machine,ustruct, time, urequests
from lora_init import *
from sensors_display import *
from aes_tools import *
from wifi_tools import *
from umqtt.simple import MQTTClient
SSID = 'Bbox-9ECEBF79'
PASSWORD = '54347A3EA6A1D6C36EF6A9E5156F7D'

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

lora_modem = lora_init()

rssi=0; chan=0; wkey=""; lumi=0.0; temp=0.0; humi=0.0; data=0

# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi, rssi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi); sf4="&field4="+str(rssi)
        url = "https://thingspeak.com/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3+sf4
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi, rssi)
    except Exception as e:
        print("Failed to send data:", e)
    
# --- Receive LoRa Packet ---
def onReceive(lora_modem,enc_payload):
    global rssi; global lumi; global temp; global humi; global data
    if len(enc_payload)==32:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(8,9,lumi,temp,humi,0)
        ack=ustruct.pack('2i2f',chan,10,0.1,32.9)  # chan, cycle, delta, thold
        enc_ack=aes_encrypt(ack,AES_KEY)
        print("send encrypted ack AES packet")
        lora_modem.println(enc_ack)  # sending ACK packet
        data=1
        lora_modem.receive()

def main():
    global rssi; global lumi; global temp; global humi; global data
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        if data:
            if connect_WiFi(SSID, PASSWORD):
                print("WiFi connected")
            send_data_to_thingspeak(lumi, temp, humi, rssi)
            time.sleep(1); data=0
            disconnect_WiFi()
        time.sleep(15)

        
        
main()

