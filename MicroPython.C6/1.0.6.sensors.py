from machine import Pin, I2C
import time
# I2C addresses for the sensors
MAX44009_I2C_ADDR = 0x4A  # Common address for MAX44009
SHT21_I2C_ADDR = 0x40     # Address for SHT21 (also known as HTU21D)

def read_max44009(i2c):
    # Read two bytes from registers 0x03 and 0x04
    data = i2c.readfrom_mem(MAX44009_I2C_ADDR, 0x03, 2)
    exponent = (data[0] & 0xF0) >> 4
    mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
    lux = (2 ** exponent) * mantissa * 0.045
    return lux

def read_sht21(i2c):

    # Trigger temperature measurement
    i2c.writeto(SHT21_I2C_ADDR, b'\xF3')
    time.sleep_ms(100)  # Wait for measurement
    raw_temp_data = i2c.readfrom(SHT21_I2C_ADDR, 2)
    raw_temp = (raw_temp_data[0] << 8) + raw_temp_data[1]
    temperature = -46.85 + 175.72 * (raw_temp / 65536.0)
    # Trigger humidity measurement
    i2c.writeto(SHT21_I2C_ADDR, b'\xF5')
    time.sleep_ms(100)  # Wait for measurement
    raw_hum_data = i2c.readfrom(SHT21_I2C_ADDR, 2)
    raw_hum = (raw_hum_data[0] << 8) + raw_hum_data[1]
    humidity = -6 + 125 * (raw_hum / 65536.0)
    return temperature, humidity

def sensors(sda, scl):
    # Initialize I2C
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=15000)  #  Attention to frequency !!!
    # Read luminosity
    luminosity = read_max44009(i2c)
    # Read temperature and humidity
    temperature, humidity = read_sht21(i2c)
    return round(luminosity,2), round(temperature,2) , round(humidity,2)
