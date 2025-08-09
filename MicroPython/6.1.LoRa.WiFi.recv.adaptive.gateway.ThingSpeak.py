from machine import Pin, I2C, SPI
import machine,ustruct, time, urequests, random
from lora_init import *
from sensors_display import *
from aes_tools import *
from wifi_tools import *
SSID = 'Bbox-9ECEBF79'
PASSWORD = '54347A3EA6A1D6C36EF6A9E5156F7D'

AES_KEY = b'smartcomputerlab'  # Replace with your actual 16-byte AES key
lora_modem = lora_init()
wkey=""; rssi=0; chan=0; wkey=""; lumi=0.0; temp=0.0; humi=0.0; data=0

def dynamic_wait(duration):
    start_time = time.ticks_ms()  # Get start time (milliseconds)
    while True:
        elapsed = time.ticks_diff(time.ticks_ms(), start_time)/1000  # Convert to seconds
        if elapsed >= duration:
            break
        # Optional: Add low-power tasks here (e.g., light sleep)
        time.sleep_ms(100)  # Small delay to reduce CPU usage
    print(f"Waited {elapsed:.2f} seconds")

# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi, rssi):
    global wkey
    try:
        swkey=str(wkey+"\0")
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi); sf4="&field4="+str(rssi)
        url = "https://thingspeak.com/update?key="+swkey+sf1+sf2+sf3+sf4

        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi, rssi)
    except Exception as e:
        print("Failed to send data:", e)
        
    
ack_num=0   
# --- Receive LoRa Packet ---
def onReceive(lora_modem,enc_payload):
    global wkey; global rssi; global lumi; global temp; global humi; global data; global ack_num
    if len(enc_payload)==32:
        rssi = lora_modem.packetRssi()
        payload=aes_decrypt(enc_payload,AES_KEY)
        chan, wkey, lumi, temp, humi = ustruct.unpack('i16s3f', payload)
        print("Received LoRa packet RSSI:"+str(rssi)); print(chan,wkey,lumi,temp,humi)
        sensors_display(8,9,lumi,temp,humi,0)
        ack_num=ack_num+1; print("ack:",ack_num)
        if ack_num%60 :
            rcycle=random.randint(5,15)
            control=0;  
            ack=ustruct.pack('3if',chan,control,rcycle,0.1) 
            enc_ack=aes_encrypt(ack,AES_KEY)
            lora_modem.println(enc_ack)  # sending ACK packet
            print("send short encrypted ack AES packet")
        else:    # sends long ACK encrypted packet every 60 packets
            cntr=0; c_def=1; c_max=64; d_min=0.01;d_max=0.2;t_low=16.0; t_high=26.0
            ack=ustruct.pack("4i4f",chan,cntr,c_def,c_max,d_min,d_max,t_low,t_high) 
            enc_ack=aes_encrypt(ack,AES_KEY)
            lora_modem.println(enc_ack)  # sending ACK packet
            print("send long encrypted ack AES packet")
        data=1
        lora_modem.receive()

def main():
    global wkey; global rssi; global lumi; global temp; global humi; global data
    ts_wait=10*1500; lastnow=0
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        now = time.ticks_ms()
        if data and now > (ts_wait+lastnow) :   # ts_wait tme between 2 ThingSpeak send
            lastnow = time.ticks_ms(); data=0
            if connect_WiFi(SSID, PASSWORD):
                print("WiFi connected")
            send_data_to_thingspeak(lumi, temp, humi, rssi)
            time.sleep(1); 
            disconnect_WiFi()     
        time.sleep(2)

main()

