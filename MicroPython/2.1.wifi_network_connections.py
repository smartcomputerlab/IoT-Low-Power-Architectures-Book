import network

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # Initialize station interface
    wlan.active(True)  # Activate Wi-Fi interface
    print(f"Connecting to Wi-Fi network: {ssid}")
    wlan.disconnect()  # disconnect if already connected 
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print("Connected to Wi-Fi!")
    print("Network configuration:")
    config = wlan.ifconfig()  # Get network configuration as a tuple
    config_dict = {
        "IP Address": config[0], "Subnet Mask": config[1],
        "Gateway": config[2], "DNS Server": config[3]
    }
    for key, value in config_dict.items():
        print(f"{key}: {value}")

    return config_dict

# Example usage
if __name__ == "__main__":
    # Replace with your Wi-Fi credentials
    SSID = 'Livebox-08B0'
    PASSWORD = 'G79ji6dtEptVTPWmZP'
    config = connect_to_wifi(SSID, PASSWORD)

