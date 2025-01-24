import network
import esp32
from machine import Pin, deepsleep, RTC
import espnow
import utime, ustruct
from sensors import *

# Function to read data from internal flash memory using NVS
def read_from_eeprom_wkey(key):
    nvs_key = esp32.NVS("storage")  # Open the NVS namespace "storage"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        print(f"Data read: {key} -> {buff}")
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None

led = Pin(15, Pin.OUT)
led.value(1)
dlen,rparam = read_from_eeprom_wkey("param")
chan,wkey,rmac=ustruct.unpack("i16s6s",rparam)
print("len:",len,"chan:",chan,"wkey:",wkey.decode(),"mac:",rmac) 
#count = count+1
   
print("len:",dlen,"chan:",chan,"wkey:",wkey,"mac:",rmac)     
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.config(txpower=8.5)
sta.config(channel=chan)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)
print("now active")
#peer= b'\x54\x32\x04\x0B\x3C\xF8'  # Replace with receiver's MAC address
#peer= b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Replace with broadcast MAC address
esp.add_peer(rmac)

#while True:
lumi,temp,humi=sensors(sda=19,scl=20)
data=ustruct.pack('i16s3f',1254,wkey,lumi,temp,humi)
esp.send(rmac, data)
utime.sleep(2)
led.value(0)
deepsleep(12*1000)
