from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensor_display import *
import time
from aes_tools import *
import random
# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
# Initialize LoRa modem
lora_modem = lora_init()
# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    if len(payload)==32:
        rssi = lora_modem.packetRssi()
        data=aes_decrypt(payload,AES_KEY)
        chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', data)
        print("Received LoRa packet:"+str(rssi))   #, payload.decode())
        cycle=random.randint(6,26)
        ack=ustruct.pack('2ifi',1234,cycle,0.01,10)  	# chan,cycle,delta,kpack
        encrypted_ack=aes_encrypt(ack,AES_KEY)
        time.sleep(0.4)                         # wait short time before ack
        lora_modem.println(encrypted_ack)  # sending ACK packet
        print("ACK packet sent")
        sensor_display(8,9,temp,humi,lumi,rssi)
    
    lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()
