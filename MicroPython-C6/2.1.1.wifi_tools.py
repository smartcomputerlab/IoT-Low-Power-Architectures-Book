import network
import time

def connect_wifi(ssid, passwd, timeout=10):
    """
    Connect to the given WiFi network using the specified SSID and password.
    :param ssid: The SSID of the WiFi network.
    :param passwd: The password of the WiFi network.
    :param timeout: Maximum time in seconds to wait for connection.
    :return: True if connected, False otherwise.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If already connected to the same network, return True
    if wlan.isconnected() and wlan.config('essid') == ssid:
        return True
    # Connect to the given SSID
    wlan.connect(ssid, passwd)
    # Wait for connection or timeout
    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            return False
        time.sleep(1)
    
    return True

def disconnect_wifi():
    """
    Disconnect from the currently connected WiFi network.
    """
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()

def scan_wifi():
    """
    Scan for available WiFi networks.
    :return: A list of tuples containing network information:
             (ssid, bssid, channel, RSSI, authmode, hidden)
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan.scan()
