from machine import Pin, I2C
import time

# Assuming you have bh1750.py in your device:
from bh1750 import BH1750

# Assuming you have bme680.py in your device:
from bme680 import BME680_I2C

def sensors(sda=8, scl=9):
    # Initialize I2C interface
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
    # Initialize BH1750 sensor (typical address: 0x23 or 0x5C)
    bh = BH1750(i2c)
    # Initialize BME680 sensor (typical addresses: 0x76 or 0x77)
    #bme = BME680_I2C(i2c=i2c, addr=0x76)
    bme = BME680_I2C(I2C(-1, Pin(scl), Pin(sda)))
    
    # Give the BME680 some time to perform measurements if required
    # (Some BME680 libraries handle this automatically.)
    time.sleep_ms(200)
    # Read luminosity from BH1750
    luminosity = bh.luminance(BH1750.CONT_HIRES_1)  # returns value in lux
    # Read temperature, humidity, pressure, gas from BME680
    # Values typically in °C, %, hPa, ohms respectively
    temperature = bme.temperature
    humidity = bme.humidity
    pressure = bme.pressure
    gas = bme.gas
    
    # Return all sensor values
    return luminosity, temperature, humidity, pressure, gas

