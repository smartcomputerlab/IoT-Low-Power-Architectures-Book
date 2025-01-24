import requests
from whisper_filter import *
THINGSPEAK_API_URL="https://api.thingspeak.com/update"
CHANNEL_API_KEY= "4K897XNNHTW7I4NO"
FIELD_NUMBER = 1

def send_to_thingspeak(message):
    try:
        payload = { f"field{FIELD_NUMBER}": message, "api_key": CHANNEL_API_KEY }
        print(f"Sending message: '{message}' to ThingSpeak on field {FIELD_NUMBER}..")
        response = requests.post(THINGSPEAK_API_URL, data=payload)
        if response.status_code == 200:
            print("Message sent to TS")
        else:
            print("Failed to send to TS")

    except Exception as e:
        print("Failed to send. Error: {e}")

def main():
    try:
            while True:
                user_input = input("")
                result = whisper_filter(user_input)
                print(result)
                if result!=None:
                    send_to_thingspeak(result)
                    print("sent")
                else:
                    print("not sent")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    
    