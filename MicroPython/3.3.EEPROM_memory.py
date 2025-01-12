import machine
import time
import ustruct

class AT24C32:
    def __init__(self, i2c, address=0x50):
        self.i2c = i2c
        self.address = address
        self._capacity = 4096  # AT24C32 has 4KB capacity

    def write(self, addr, buff):
        if not isinstance(buff, (bytes, bytearray)):
            raise ValueError("Buffer must be of type 'bytes' or 'bytearray'")
        if addr < 0 or addr + len(buff) > self._capacity:
            raise ValueError("Address out of range")
        for i in range(len(buff)):
            self.i2c.writeto(self.address, bytes([addr >> 8, addr & 0xFF, buff[i]]))
            time.sleep(0.01)  # EEPROM write delay
            addr += 1

    def read(self, addr, length):
        if addr < 0 or addr + length > self._capacity:
            raise ValueError("Address out of range")
        self.i2c.writeto(self.address, bytes([addr >> 8, addr & 0xFF]))
        return self.i2c.readfrom(self.address, length)

    def capacity(self):
        return self._capacity

def main():
    I2C_SCL = 9; I2C_SDA = 8
    i2c = machine.I2C(0, scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA))
    eeprom = AT24C32(i2c)
    test_address = 0x00  # Starting address in EEPROM
    ts_wkey = "YOX31M0EDKO0JATK"  # Data to write
    wifi_chan =1
    
    mac_str="54:32:04:0B:3C:F8"
    mac_parts = mac_str.split(":")
    mac_bytes = bytes(int(part, 16) for part in mac_parts)
    print(mac_str); print(mac_bytes)
    print("Writing to EEPROM...")
    print("Write data:", wifi_chan,ts_wkey,mac_str)
    wparam = ustruct.pack("i16s6s",wifi_chan,ts_wkey,mac_bytes)
    eeprom.write(test_address, wparam)
    print("Reading from EEPROM...")
    rparam = eeprom.read(test_address, len(wparam))
    rwifi_chan,rts_wkey,rmac=ustruct.unpack("i16s6s",rparam)
    print("Read data:", rwifi_chan,rts_wkey.decode('utc-8'),rmac)
    print("Device MAC Address:", ":".join(["{:02X}".format(byte) for byte in rmac]))
    print("EEPROM Capacity:", eeprom.capacity(), "bytes")

if __name__ == "__main__":
    main()
    