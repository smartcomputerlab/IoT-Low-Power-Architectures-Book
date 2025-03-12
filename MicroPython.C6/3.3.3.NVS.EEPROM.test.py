from eeprom_tools import *
from nvs_tools import *
from machine import Pin, I2C
import time
boot_button = Pin(18, Pin.IN, Pin.PULL_UP)  # GPIO 0 is connected to BOOT
I2C_SDA = 19 ; I2C_SCL = 20  
try:
    i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=100000)  # 100kHz speed
    time.sleep(1)
except Exception as e:
    print("Error initializing I2C:", e)
    raise

def scan_i2c():
    devices = i2c.scan()
    if devices:
        print("I2C devices found:", [hex(device) for device in devices])
    else:
        print("No I2C devices found!")
    return devices

EEPROM_ADDRESSES = [0x50] #, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57]

def detect_eeprom():
    devices = scan_i2c()
    found_eeproms = [addr for addr in EEPROM_ADDRESSES if addr in devices]
    return found_eeproms

prot_key="0123456789abcdef"

if detect_eeprom() and boot_button.value() == 0:  # Button pressed (LOW)
    print("AT24C attached and BOOT button pressed!")
    saved_prot_key = eeprom_read_prot_key()
    if prot_key==saved_prot_key :
        print("EEPROM prot key verified!")
        save_credentials("dummyAP","dummypassword")
        ssid,password=eeprom_read_ssid_pass()
        save_credentials(ssid,password)
        print("SSID: ", ssid);
        print("Password: ",password)
        
        