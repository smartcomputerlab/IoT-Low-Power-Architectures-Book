from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensor_display import *
import time
from aes_tools import *
AES_KEY = b'smartcomputerlab'

# Initialize LoRa modem
lora_modem = lora_init()

def main():
    #lora_modem.receive()
    while True:
        if lora_modem.receivedPacket():  # Check if a packet has been received
            encrypted_payload = lora_modem.readPayload()  # Read the payload of the received packet
            payload=aes_decrypt(encrypted_payload,AES_KEY)
            rssi = lora_modem.packetRssi()
            chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', payload)
            print("Received LoRa packet:"+str(rssi))   #, payload.decode())
            sensor_display(temp,humi,lumi,rssi,0)
            chan=123; cycle=10; delta=0.1;kpack=20
            ack=ustruct.pack('2ifi', chan,cycle,delta,kpack)
            encrypted_ack=aes_encrypt(ack,AES_KEY)
            print("sending encrypted ACK packet")
            time.sleep(0.8)
            lora_modem.println(encrypted_ack)  # sending ACK packet
        time.sleep(0.01)
        
main()
