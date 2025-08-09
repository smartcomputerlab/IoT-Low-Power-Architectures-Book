# at24_tools.py
import machine
import time
import ustruct

class AT24C32:
    def __init__(self, i2c, address=0x50):
        self.i2c = i2c
        self.address = address
        self._capacity = 4096  # AT24C32 has 4KB capacity

    def write_at24(self, addr, buff):
        if not isinstance(buff, (bytes, bytearray)):
            raise ValueError("Buffer must be of type 'bytes' or 'bytearray'")
        if addr < 0 or addr + len(buff) > self._capacity:
            raise ValueError("Address out of range")
        for i in range(len(buff)):
            self.i2c.writeto(self.address, bytes([addr >> 8, addr & 0xFF, buff[i]]))
            time.sleep(0.01)  # EEPROM write delay
            addr += 1

    def read_at24(self, addr, length):
        if addr < 0 or addr + length > self._capacity:
            raise ValueError("Address out of range")
        self.i2c.writeto(self.address, bytes([addr >> 8, addr & 0xFF]))
        return self.i2c.readfrom(self.address, length)

    def capacity(self):
        return self._capacity

