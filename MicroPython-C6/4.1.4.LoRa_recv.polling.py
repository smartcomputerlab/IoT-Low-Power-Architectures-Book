from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensor_display import *
import time
# Initialize LoRa modem
lora_modem = lora_init()
def main():
    #lora_modem.receive()
    while True:
        if lora_modem.receivedPacket():  # Check if a packet has been received
            payload = lora_modem.readPayload()  # Read the payload of the received packet
            rssi = lora_modem.packetRssi()
            chan, wkey, temp, humi, lumi = ustruct.unpack('i16s3f', payload)
            print("Received LoRa packet:"+str(rssi))   #, payload.decode())
            sensor_display(temp,humi,lumi,rssi,0)
            chan=123; cycle=10; delta=0.1;kpack=20
            ack=ustruct.pack('2ifi', chan,cycle,delta,kpack)
            print("sending ACK packet")
            lora_modem.println(ack)  # sending ACK packet
        time.sleep(0.1)
        
main()
