from machine import Pin, I2C, SPI, UART
import ustruct
from lora_init import *
import time

# Initialize LoRa modem
lora_modem = lora_init()
uart = UART(1, baudrate=9600, rx=0, tx=1)

# --- Receive LoRa Packet ---
def onReceive(lora_modem,payload):
    rssi = lora_modem.packetRssi()
    #print("Waiting for LoRa packets...")
    print("Received LoRa packet:"+payload.decode('uft-8'))  #, payload.decode())
    uart.write(payload)
    lora_modem.println("ACK_packet")  # sending ACK packet
    lora_modem.receive()

def main():

    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()
