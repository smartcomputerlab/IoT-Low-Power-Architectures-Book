#!/usr/bin/python3
import requests, time
from piper_play import *

THINGSPEAK_READ_API_URL = "https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/{FIELD_NUMBER}.json"
CHANNEL_ID = "1697980"  # Replace with your ThingSpeak channel ID
READ_API_KEY = " V9GT1RN2FIP0YRAY"  # Replace with your ThingSpeak read API key
FIELD_NUMBER = 1  # Field number to read

# Function to read the latest message from ThingSpeak
def read_from_thingspeak():
    try:
        url = THINGSPEAK_READ_API_URL.format(CHANNEL_ID=CHANNEL_ID, FIELD_NUMBER=FIELD_NUMBER)
        params = {
            "api_key": READ_API_KEY,
            "results": 1  # Retrieve the latest entry
        }
        print(f"Reading the latest message from ThingSpeak on field {FIELD_NUMBER}...")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if "feeds" in data and len(data["feeds"]) > 0:
                latest_message = data["feeds"][0][f"field{FIELD_NUMBER}"]
                print(f"Latest message: {latest_message}")
                return latest_message
            else:
                print("No data available on ThingSpeak.")
                return ""
        else:
            print(f"Failed to read message. HTTP status code: {response.status_code}, Response: {response.text}")
            return ""

    except Exception as e:
        print(f"Error reading message from ThingSpeak: {e}")
        return ""

def main():
    target_port = 8888       # Replace with the target port number
    voix = “female”
    # Start receiving messages
    while True:
        msg=read_from_thingspeak()
        msg = msg + "\n"
        piper_play(msg,voix)
        time.sleep(12)

main()
