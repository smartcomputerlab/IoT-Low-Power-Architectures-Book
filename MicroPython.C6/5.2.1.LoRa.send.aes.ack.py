import time, ustruct
from machine import I2C, Pin, deepsleep, RTC
from sensors import *
from read_battery import *
from lora_init import lora_init
from aes_tools import *
AES_KEY = b'smartcomputerlab'

delta=0.04
rtc = RTC()

def read_stemp():
    data = rtc.memory()
    if not data:
        stemp = 20.0
    else:
        stemp = float(data)
    return stemp

def write_stemp(stemp):
    rtc.memory(str(stemp).encode())
              
# Initialize the LED pin
led = Pin(15, Pin.OUT)
# Initialize LoRa communication
lora = lora_init()

def onReceive(lora_modem,ack):
    print("Received LoRa packet:")
    decrypted_ack=aes_decrypt(ack,AES_KEY)
    chan,cycle,delta,kpack=ustruct.unpack('2ifi',decrypted_ack)
    print(chan);print(cycle);print(delta);print(kpack)
    time.sleep(0.1);lora.sleep();time.sleep(0.1)
    #deepsleep(10*1000)
    
# Function to send sensor data over LoRa
def send_lora_data(b,t,h,l):
    try:
        data = ustruct.pack('i16s7f', 1254,'smartcomputerlab',b,t,h,l,0.0,0.0,0.0)
        encrypted_data=aes_encrypt(data,AES_KEY)
        lora.println(encrypted_data)
        print("LoRa packet sent successfully.")
    except Exception as e:
        print("Failed to send LoRa packet:", e)

def main():
    lora.onReceive(onReceive)
    lora.receive()
    while True:
        battery=read_battery()
        print("Battery", battery, "V")
        lumi, temp, humi = sensors(sda=19, scl=20)
        print(lumi, temp, humi)
        stemp=read_stemp()
        print(temp,stemp)
        if(abs(temp-stemp)>delta):
            led.value(1)
            send_lora_data(battery,temp, humi, lumi)
            write_stemp(temp)
            lora.receive()
            time.sleep(2)
            led.value(0)
            
        lora.sleep()
        time.sleep(6)
        #deepsleep(6*1000)
# Run the main program
main()
