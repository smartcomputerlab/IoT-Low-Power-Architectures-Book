from machine import Pin, RTC, deepsleep
import ubinascii, urequests
import machine
from wifi_tools import *
from sensors import sensors
import time
# WiFi credentials
SSID = 'PhoneAP'
PASSWORD = 'smartcomputerlab'
led=Pin(15,Pin.OUT)
rtc = RTC()             # instantiates RTC memory

# Function to send data to ThingSpeak
def send_data_to_thingspeak(lumi, temp, humi):
    try:
        sf1="&field1="+str(lumi); sf2="&field2="+str(temp); sf3="&field3="+str(humi)
        url = "https://api.thingspeak.com/update?key=YOX31M0EDKO0JATK"+sf1+sf2+sf3
        response = urequests.get(url)
        response.close()
        print("Data sent to ThingSpeak:", lumi, temp, humi)
    except Exception as e:
        print("Failed to send data:", e)

def main():
    delta=0.05
    led.value(0)
    # Retrieve cycle counter from RTC memory
    rtc_mem = rtc.memory()
    if len(rtc_mem) == 0:
        stemp = 20.0
    else:
        stemp = float(rtc_mem.decode())
        
    lumi, temp, humi = sensors(sda=19, scl=20)
    if (abs(stemp-temp)> delta):
        led.value(1)
        rtc.memory(str(temp).encode())
        # Initialize WiFi and connect to access point
        connect_wifi(SSID, PASSWORD)
        print("WiFi connected")
        send_data_to_thingspeak(lumi, temp, humi)
        time.sleep(1)
        led.value(0)
    time.sleep(2)          # to enable interruption   
    deepsleep(15*1000)

# Run the main function
main()
