from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensors_display import *
import time
from aes_tools import *
AES_KEY = b'smartcomputerlab'
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
    lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()
