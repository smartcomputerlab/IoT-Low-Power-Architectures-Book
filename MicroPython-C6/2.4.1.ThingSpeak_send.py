from machine import Pin
import ubinascii, urequests
import machine
from wifi_tools import *
from sensors import sensors
import time
# WiFi credentials
SSID = 'PhoneAP'
PASSWORD = 'smartcomputerlab'
led=Pin(15,Pin.OUT)

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
            send_data_to_thingspeak(lumi, temp, humi)
            time.sleep(1)
            led.value(0)
            time.sleep(15)      # temie between two send requests to thingspeak
        time.sleep(1)

# Run the main function
main()
