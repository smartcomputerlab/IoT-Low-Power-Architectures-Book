import time, ustruct
from machine import I2C, Pin, deepsleep
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

def onReceive(lora_modem,payload):
    if len(payload)==16:
        global rchan; global cycle; global delta; global kpack; global temp
        ack=aes_decrypt(payload,AES_KEY)
        rchan, cycle, delta, kpack = ustruct.unpack('2ifi', ack)
        if chan==rchan :
            rtc_store_param(cycle,delta,kpack)
            time.sleep(0.1); lora.sleep();time.sleep(0.1)
            led.value(0)
            deepsleep(cycle*1000)
 
def send_lora_data(t, h, l):
    try:
        # Create the message with temperature, humidity, and luminosity
        message = f"T:{t:.2f},H:{h:.2f},L:{l:.2f}"
        print("Sending LoRa packet:", message)
        # prepare data packet with bytes
        data = ustruct.pack('i16s3f', 1254,'here_is_your_key',t,h,l)  # put valid wkey
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
#while True:
    led.value(1)
    cycle,delta,kpack=rtc_load_param()
    counter=rtc_load_counter()
    lumi, temp, humi = sensors(sda=19, scl=20)
    print(lumi,temp,humi)
    stemp=rtc_load_sensor()
    print("Stored temp",stemp); print("Cycle counter",counter); 
    if (abs(temp-stemp)>delta or ((counter%kpack)==0)):
        send_lora_data(temp, humi, lumi);
        rtc_store_sensor(temp)
        time.sleep(2)
        cycle,delta,kpack=rtc_load_param()
    counter=counter+1
    rtc_store_counter(counter)
    lora.sleep(); time.sleep(2); led.value(0)
    deepsleep(cycle*1000)

main()
