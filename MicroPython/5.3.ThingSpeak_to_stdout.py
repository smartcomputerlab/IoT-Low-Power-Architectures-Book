# ./thingspeak_to_stdout.py | ./piper -m models/GB/female.onnx --output-raw | \
# aplay -r 16000 -f S16_LE -t raw -
#!/usr/bin/python3
import socket
import serial, tempfile, os
import subprocess
import requests, time

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

# function for when a message is received
def echo_udp_message(msg):
    try:
        msg = msg + "\n"
        print(f"Received message: {msg}")
        with tempfile.NamedTemporaryFile(delete=False, mode='w',prefix='mqtt_', suffix='.txt') as temp_file:
            temp_file.write(msg)
            print(f"Message written to temporary file: {temp_file}")
            # Read back from the temporary file and use echo command
        with open(temp_file.name, 'r') as file:
            file_content = file.read()
            print(f"Read from temporary file: {file_content}")
            os.remove(temp_file.name)
            os.system(f'echo "{file_content}"')

    except Exception as e:
        print(f"Error handling message: {e}")

def main():
    target_port = 8888       # Replace with the target port number
    # Start receiving messages
    while True:
        message=read_from_thingspeak()
        echo_udp_message(message)
        time.sleep(2)

main()
