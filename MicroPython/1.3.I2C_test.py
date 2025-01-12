from machine import Pin, I2C

# Configure I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8))  # I2C bus 0 with custom pins

# Scan for I2C devices
devices = i2c.scan()
print("I2C devices found:", devices)

# Assuming a device is found at address 0x3C
device_address = 0x3C

# Write to the device
data_to_write = bytearray([0x00, 0xFF])  # Example data
i2c.writeto(device_address, data_to_write)

# Read from the device
num_bytes = 2
data_read = i2c.readfrom(device_address, num_bytes)
print("Data read:", data_read)
