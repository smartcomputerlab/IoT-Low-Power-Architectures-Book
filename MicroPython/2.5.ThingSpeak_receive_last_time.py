import urequests
import network
import time
from wifi_tools import *

SSID = 'Livebox-08B0'
PASSWORD = 'G79ji6dtEptVTPWmZP'
# ThingSpeak API details
THINGSPEAK_CHANNEL_ID = '1538804'          # Replace with your ThingSpeak channel ID
THINGSPEAK_API_KEY = '20E9AQVFW7Z6XXOM'    # Replace with your ThingSpeak read API key

# Function to fetch the last record from ThingSpeak
def fetch_last_record():
    url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?results=1"
    print(f"Fetching last record from {url}")
    try:
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            feeds = data.get("feeds", [])
            if feeds:
                last_record = feeds[0]
                created_at = last_record.get("created_at", "Unknown")
                print(f"Last record timestamp: {created_at}")
                return created_at
            else:
                print("No records found in the channel.")
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except Exception as e:
        print("Error fetching data:", e)
    return None

# Main program
def main():
    connect_WiFi(SSID,PASSWORD)
    last_timestamp = fetch_last_record()
    if last_timestamp:
        print("The last record was created at:", last_timestamp)
    else:
        print("Could not retrieve the last record.")

main()
