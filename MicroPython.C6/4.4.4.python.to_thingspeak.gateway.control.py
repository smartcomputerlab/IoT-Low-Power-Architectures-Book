"""    :param api_key: Your ThingSpeak write API key
    :param field1: Value for field1
    :param field2: Value for field2
    :param field3: Value for field3
    """
    url = "https://api.thingspeak.com/update"
    data = {
        'api_key': api_key,
        'field1': field1,
        'field2': field2,
        'field3': field3
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Data successfully sent to ThingSpeak.")
    else:
        print(f"Failed to send data. HTTP error code: {response.status_code}")
if __name__ == "__main__":
    # Replace with your ThingSpeak channel write API key
    THINGSPEAK_API_KEY = "3IN09682SQX3PT4Z"
    print("Enter three values to send to ThingSpeak:")
    try:
        field1 = int(input("Enter cycle integer value (seconds) for field1: "))
        field2 = float(input("Enter delta float value (difference) for field2: "))
        field3 = int(input("Enter kpack integer value (rate) for field3: "))
        send_to_thingspeak(THINGSPEAK_API_KEY, field1, field2, field3)
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        