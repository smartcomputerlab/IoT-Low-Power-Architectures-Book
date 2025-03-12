from machine import Pin, I2C
import time
# I2C addresses for the sensors
MAX44009_I2C_ADDR = 0x4A  # Common address for MAX44009
SHT21_I2C_ADDR = 0x40     # Address for SHT21 (also known as HTU21D)

def read_max44009(i2c):
    """
    Read luminosity (lux) from the MAX44009 sensor.
    According to the datasheet:
    The luminosity data is in 2 registers:
    - 0x03: Exponent and high part of Mantissa
    - 0x04: Low part of Mantissa
    Lux calculation:
    exponent = (data[0] & 0xF0) >> 4
    mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
    lux = (2 ** exponent) * mantissa * 0.045
    """
    # Read two bytes from registers 0x03 and 0x04
    data = i2c.readfrom_mem(MAX44009_I2C_ADDR, 0x03, 2)
    exponent = (data[0] & 0xF0) >> 4
    mantissa = ((data[0] & 0x0F) << 4) | (data[1] & 0x0F)
    lux = (2 ** exponent) * mantissa * 0.045
    return lux

def read_sht21(i2c):
    """
    Read temperature and humidity from the SHT21 sensor.
    SHT21 commands:
    - Trigger Temperature Measurement, No Hold Master: 0xF3
    - Trigger Humidity Measurement, No Hold Master: 0xF5
    After writing the command, we must wait for the measurement.
    Typical max measurement times:
    - Temperature: up to 50 ms
    - Humidity: up to 16 bit resolution ~ 29 ms
    Formulas from datasheet:
    Temperature (°C) = -46.85 + 175.72 * (raw_temp / 65536)
    Humidity (%RH) = -6 + 125 * (raw_humidity / 65536)
    """
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
    """
    Initialize I2C on given SDA, SCL pins,
    read luminosity from MAX44009 and temperature/humidity from SHT21,
    and return them as a tuple:
    (luminosity, temperature, humidity)
    """
    # Initialize I2C
    i2c = I2C(scl=Pin(scl), sda=Pin(sda), freq=100000)
    # Read luminosity
    luminosity = read_max44009(i2c)
    # Read temperature and humidity
    temperature, humidity = read_sht21(i2c)
    return luminosity, temperature, humidity
    