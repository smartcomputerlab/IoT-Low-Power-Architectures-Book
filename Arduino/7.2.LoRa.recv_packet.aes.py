from machine import Pin, I2C, SPI
import ustruct, time
from lora_init import *
from sensors_display import *
from aes_tools import *

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
lora_modem = lora_init()
# --- Receive LoRa Packet ---
def onReceive(lora_modem,enc_payload):
    if len(enc_payload)==32:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(8,9,lumi,temp,humi,0)
        ack=ustruct.pack('2i2f',chan,10,0.1,32.9)  # chan, cycle, delta, kpack
        enc_ack=aes_encrypt(ack,AES_KEY)
        lora_modem.println(enc_ack)  # sending ACK packet
        lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()

