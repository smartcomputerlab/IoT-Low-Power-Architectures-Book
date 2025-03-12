from machine import Pin, I2C, SPI
import ustruct,urequests
from lora_init import *
from sensors_display import *
import time
from aes_tools import *
from wifi_tools import *
# WiFi credentials
SSID = 'PhoneAP'
PASS = 'smartcomputerlab'
AES_KEY = b'smartcomputerlab'

 # Function to send data to ThingSpeak
def send_data_to_thingspeak(wkey,lumi,temp,humi,bat):
    try:
        connect_wifi(SSID,PASS)
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi); sf4="&field4="+str(bat)
        #url = "http://2.12.92.92:443/update?key=HEU64K3PGNWG36C4"+sf1+sf2+sf3
        url = "https://api.thingspeak.com/update?key="+wkey+sf1+sf2+sf3+sf4
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi, bat)
        pack=1
    except Exception as e:
        print("Failed to send data:", e)

# Initialize LoRa modem
lora_modem = lora_init()
# --- Receive LoRa Packet ---
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
    send_data_to_thingspeak("YOX31M0EDKO0JATK",lumi,temp,humi,battery)
    lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(6)
        print("in the loop")
        
main()
