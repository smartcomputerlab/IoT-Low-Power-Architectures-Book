from machine import Pin, I2C, SPI
from wifi_tools import *
import ustruct, urequests, time, random
from lora_init import *
from sensor_display import *
from aes_tools import *
from umqtt.simple import MQTTClient
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'

# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

# Initialize LoRa modem
lora_modem = lora_init()

chan=1234; wkey="smartcomputerlab"; temp=20.0; humi=50.0; lumi=100.0; pack=0

 # Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey,lumi,temp,humi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        #url = "http://2.12.92.92:443/update?key=HEU64K3PGNWG36C4"+sf1+sf2+sf3
        url = "https://107.23.148.232/update?key="+wkey+sf1+sf2+sf3
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
        ack=ustruct.pack('2ifi',1234,cycle,0.1,10)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.8)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(temp,humi,lumi,rssi,0)
    
    lora_modem.receive()

def main():
    global pack; global wkey; global temp; global humi; global lumi; global pack
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        print("in the loop")
        if pack==1 :
            connect_WiFi(SSID,PASS)
            send_data_to_thingspeak("YOX31M0EDKO0JATK",lumi,temp,humi)
            time.sleep(1)
            pack = 0
            
        time.sleep(4)
        
main()