import machine, ustruct
import esp32

# Function to write data to internal flash memory using NVS (Non-Volatile Storage)
def write_to_eeprom_wkey(key, value):
    nvs_key = esp32.NVS("storage")  # Open the NVS namespace "storage"
    nvs_key.set_blob(key, value)  # Store a byte array (blob) with a key
    nvs_key.commit()  # Commit the changes
    print(f"Data written: {key} -> {value}")

# Function to read data from internal flash memory using NVS
def read_from_eeprom_wkey(key):
    nvs_key = esp32.NVS("storage")  # Open the NVS namespace "storage"
    try:
        buff = bytearray(32)
        value = nvs_key.get_blob(key,buff)  # Retrieve the byte array (blob) using the key
        print(f"Data read: {key} -> {buff}")
        return value,buff
    except OSError:
        print(f"Key '{key}' not found in EEPROM.")
        return None

# Main program to demonstrate write and read functionality
def main():
    key = "param"  # Key for the data
    ts_wkey = "YOX31M0EDKO0JATK"  # Data to write
    wifi_chan =1
    #mac = b'\x54\x32\x04\x0B\x3C\xF8'
    mac = b'T2\x04\x0b<\xf8'
    wparam = ustruct.pack("i16s6s",wifi_chan,ts_wkey,mac)
    print("Writing to internal EEPROM...")
    write_to_eeprom_wkey(key, wparam)
    print("Reading from internal EEPROM...")
    len,rparam = read_from_eeprom_wkey(key)
    if len:
        chan,wkey,rmac=ustruct.unpack("i16s6s",rparam)
        print("len:",len,"chan:",chan,"wkey:",wkey.decode(),"mac:",rmac) 

if __name__ == "__main__":
    main()
    