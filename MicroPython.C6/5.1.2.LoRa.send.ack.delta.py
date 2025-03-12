import time, ustruct
from machine import I2C, Pin, deepsleep, RTC
from sensors import *
from read_battery import *
from lora_init import lora_init
delta=0.1
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
              
led = Pin(15, Pin.OUT)
lora = lora_init()

def onReceive(lora_modem,payload):
    print("Received LoRa packet:")
    chan,cycle,delta,kpack=ustruct.unpack('2ifi',payload)
    print(chan,cycle,delta,kpack)
    time.sleep(0.1);lora.sleep();time.sleep(0.1)
    #deepsleep(10*1000)
    
def send_lora_data(b,t,h,l):
    try:
        message = f"T:{t:.2f},H:{h:.2f},L:{l:.2f}"
        print("Sending LoRa packet:", message)
        data = ustruct.pack('i16s7f', 1254,'smartcomputerlab',b,t,h,l,0.0,0.0,0.0)
        lora.println(data)
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
            lora.receive();time.sleep(2)
            led.value(0)
            
        lora.sleep()
        time.sleep(1)
        deepsleep(6*1000)
# Run the main program
main()
