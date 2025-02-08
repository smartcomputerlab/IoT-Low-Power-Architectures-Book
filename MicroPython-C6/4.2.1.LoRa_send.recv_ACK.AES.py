import time, ustruct
from machine import I2C, Pin, deepsleep
from sensors import *
from lora_init import lora_init
from aes_tools import *
AES_KEY = b'smartcomputerlab'

# Initialize the LED pin
led = Pin(15, Pin.OUT)
# Initialize LoRa communication
lora = lora_init()

def onReceive(lora_modem,payload):
    print("Received LoRa packet:")
    decrypted_payload=aes_decrypt(payload,AES_KEY)
    chan,cycle,delta,kpack=ustruct.unpack('2ifi',decrypted_payload)
    print(chan);print(cycle);print(delta);print(kpack)
    time.sleep(0.1)
    lora.sleep()
    time.sleep(0.1)
    #deepsleep(10*1000)
    
# Function to send sensor data over LoRa
def send_lora_data(t, h, l):
    try:
        # prepare data packet with bytes
        data = ustruct.pack('i16s3f', 1254,'smartcomputerlab',t,h,l)
        encrypted_data=aes_encrypt(data,AES_KEY)
        lora.println(encrypted_data)
        print("LoRa packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)

def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        led.value(1)
        lum, temp, hum = sensors(sda=19, scl=20)
        print("Luminosity:", lum, "lux"); print("Temperature:", temp, "C");print("Humidity:", hum, "%")
        # Send sensor data over LoRa
        send_lora_data(temp, hum, lum)
        lora.receive()
        time.sleep(2); led.value(0)
        lora.sleep(); time.sleep(5)
        #deepsleep(10*1000)

# Run the main program
main()
