from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensor_display import *
import time

# Initialize LoRa modem
lora_modem = lora_init()

# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    rssi = lora_modem.packetRssi()
    #print("Waiting for LoRa packets...")
    chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', payload)
    print("Received LoRa packet:"+str(rssi))   #, payload.decode())
    sensor_display(temp,humi,lumi,rssi)
    lora_modem.println("ACK_packet")  # sending ACK packet
    lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()
