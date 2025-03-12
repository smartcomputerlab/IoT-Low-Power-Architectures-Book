from machine import Pin, ADC
import ubinascii, urequests
import machine
from wifi_tools import *
from sensors import sensors
import time
from machine import Pin, ADC
SSID = 'PhoneAP'
PASSWORD = 'smartcomputerlab'
led=Pin(15,Pin.OUT)

def read_battery():
    bat = ADC(Pin(0))
    bat.atten(ADC.ATTN_11DB)      #Full range: 3.3v
    battery = bat.read()*8.12/4096
    return battery
# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi, bat):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi); sf4="&field4="+str(bat)
        url = "https://api.thingspeak.com/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3+sf4
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi, bat)
    except Exception as e:
        print("Failed to send data:", e)

def main():
    delta=0.01           # temperature difference
    stemp=20.0
    while True:
        lumi, temp, humi = sensors(sda=19, scl=20)
        if (abs(stemp-temp)> delta):
            led.value(1)
            stemp=temp
            # Initialize WiFi and connect to access point
            connect_wifi(SSID, PASSWORD)
            print("WiFi connected")
            bat=read_battery()
            send_data_to_thingspeak(lumi, temp, humi, bat)
            time.sleep(1)
            led.value(0)
            time.sleep(15)      # temie between two send requests to thingspeak
        time.sleep(1)

# Run the main function
main()

