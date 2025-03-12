from machine import Pin, I2C, SPI
import ustruct
from lora_init import *
from sensors_display import *
import time

lora_modem = lora_init()

def onReceive(lora_modem,payload):
    rssi = lora_modem.packetRssi()
    #print("Waiting for LoRa packets...")
    chan, wkey, battery, temp, humi, lumi, s5,s6,s7 = ustruct.unpack('i16s7f', payload)
    print("Received LoRa packet:"+str(rssi))   #, payload.decode())
    sensors_display(19,20,temp,humi,lumi,rssi,battery,0)
    chan=123; cycle=10; delta=0.1;kpack=20
    ack=ustruct.pack('2ifi', chan,cycle,delta,kpack)
    print("sending ACK packet")
    lora_modem.println(ack)  # sending ACK packet
    lora_modem.receive()

def main():
    lora_modem.onReceive(onReceive)
    lora_modem.receive()
    while True:
        time.sleep(2)
        print("in the loop")
        
main()
---------------------------------------------------------------------------------------------------
# sensors_display.py
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

def sensors_display(sda, scl,temperature, humidity,luminosity,rssi, bat, duration):
    # Initialize I2C bus
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
    width = 128; height = 64
    # Initialize the OLED display
    oled = SSD1306_I2C(width, height, i2c)
    oled.fill(0)
    oled.text("Sensor readings", 0, 0)
    oled.text("Lux: {:.2f}".format(luminosity), 0, 16)
    oled.text("Temp: {:.2f}".format(temperature), 0, 26)
    oled.text("Humi: {:.2f}".format(humidity), 0, 36)
    oled.text("Rssi: {:d}".format(rssi), 0, 46)
    oled.text("Bat: {:.2f}".format(bat), 0, 56)
    oled.show()
    if duration:
        time.sleep(duration)
        oled.poweroff()
        