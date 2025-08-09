# nvs_tools.py
import machine, ustruct
import esp32

# Function to write data to internal flash memory using NVS (Non-Volatile Storage)
def write_nvs_ts(key, value):
    nvs_key = esp32.NVS("thingspeak")  # Open the NVS namespace "thingspeak"
    nvs_key.set_blob(key, value)  # Store a byte array (blob) with a key
    nvs_key.commit()  # Commit the changes

# Function to read data from internal flash memory using NVS
def read_nvs_ts(key):
    nvs_key = esp32.NVS("thingspeak")  # Open the NVS namespace "thingspeak"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None
    
# Function to write data to internal flash memory using NVS (Non-Volatile Storage)
def write_nvs_power(key, value):
    nvs_key = esp32.NVS("power")  # Open the NVS namespace "thingspeak"
    nvs_key.set_blob(key, value)  # Store a byte array (blob) with a key
    nvs_key.commit()  # Commit the changes

# Function to read data from internal flash memory using NVS
def read_nvs_power(key):
    nvs_key = esp32.NVS("power")  # Open the NVS namespace "thingspeak"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None

