import urequests
import time
from wifi_tools import *
# WiFi credentials
SSID = 'PhoneAP'
PASSWORD = 'smartcomputerlab'
# ThingSpeak API details
THINGSPEAK_CHANNEL_ID = '1538804'          # Replace with your ThingSpeak channel ID
THINGSPEAK_READ_API_KEY = '20E9AQVFW7Z6XXOM'       # Replace with your ThingSpeak read API key
THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json'

# Function to read data from ThingSpeak
def read_data_from_thingspeak():
    try:
        url = f"{THINGSPEAK_URL}?api_key={THINGSPEAK_READ_API_KEY}&results=1"
        response = urequests.get(url)
        data = response.json()
        response.close()
        # Extract the latest feed (last entry)
        feed = data['feeds'][0]
        created_at=feed.get(“created_at”, “Unknown”)
        print(f"Last record timestamp: {created_at}")
        luminosity = feed['field1']
        temperature = feed['field2']
        humidity = feed['field3']
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("Luminosity:", luminosity)
        return luminosity,temperature, humidity
    except Exception as e:
        print("Failed to retrieve data:", e)
        return None, None, None

# Main program
def main():
    connect_wifi("PhoneAP","smartcomputerlab")
    while True:
        # Read and print the data from ThingSpeak
        luminosity, temperature, humidity = read_data_from_thingspeak()
        
        if temperature and humidity and luminosity:
            print(f"Read from ThingSpeak - Luminosity: {luminosity}, Temperature: {temperature}, Humidity: {humidity}")
        # Delay before the next read (e.g., every 15 seconds)
        time.sleep(15)

# Run the main program
main()
