from machine import Pin, I2C
# Define I2C pins
SCL_PIN = 20             # or 7 : low power (yellow)
SDA_PIN = 19             # or 6 : low_power (yellow)
# Initialize I2C
i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))
# Scan for devices
devices = i2c.scan()
if devices:
    print("I2C devices found at addresses:", [hex(device) for device in devices])
else:
    print("No I2C devices found")
    