import time, ustruct
from machine import I2C, Pin, deepsleep, ADC
from sensors import sensors
from lora_init import *
from aes_tools import *
from rtc_tools import *
# AES encryption settings
AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key

led = Pin(15, Pin.OUT)
lora = lora_init()
chan=1234; rchan=1234; cycle=10; delta=0.01;  kpack=10
stemp=20.0

def read_battery():
    bat = ADC(Pin(0))
    bat.atten(ADC.ATTN_11DB)      #Full range: 3.3v
    battery = bat.read()*8.12/4096
    return battery

def onReceive(lora_modem,payload):
    if len(payload)==16:
        led.value(0)
        #global rchan; global cycle; global delta; global kpack; global temp
        ack=aes_decrypt(payload,AES_KEY)
        rchan, cycle, delta, kpack = ustruct.unpack('2ifi', ack)
        if chan==rchan :
            rtc_store_param(cycle,delta,kpack)
            time.sleep(0.1); lora.sleep();time.sleep(0.1)
            led.value(0)
            lora.receive()
            deepsleep(cycle*1000)

def send_lora_data(t,h,l,b):
    try:
        data = ustruct.pack('i16s7f', 1254,'here_is_your_key',b,t,h,l,0.0,0.0,0.0)  # put valid wkey
        encrypted_data=aes_encrypt(data,AES_KEY)
        lora.println(encrypted_data)
        time.sleep(0.1)        # attention: in sender sime this delay must be much longer
        print("LoRa packet sent successfully.")
        lora.receive()
    except Exception as e:
        print("Failed to send LoRa packet:", e)

def main():
    lora.onReceive(onReceive)
    lora.receive()
    
    while True:
        cycle,delta,kpack=rtc_load_param()
        counter=rtc_load_counter()
        lumi, temp, humi = sensors(sda=19, scl=20)
        print(lumi,temp,humi)
        stemp=rtc_load_sensor()
        print(stemp,temp); print("Cycle counter",counter); 
        if (abs(temp-stemp)>delta or ((counter%kpack)==0)):
            led.value(1)
            battery=read_battery()
            send_lora_data(temp, humi, lumi, battery);
            rtc_store_sensor(temp)
            time.sleep(2)
            #cycle,delta,kpack=rtc_load_param()
            led.value(0)
            
        counter=counter+1
        rtc_store_counter(counter)
        lora.sleep(); time.sleep(2); 
    #deepsleep(cycle*1000)

main()
