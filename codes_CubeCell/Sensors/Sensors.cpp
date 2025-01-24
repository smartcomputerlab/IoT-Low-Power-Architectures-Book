#include "Sensors.h"

// SHT21 command constants
#define SHT21_TEMP_HOLD 0xE3
#define SHT21_HUMIDITY_HOLD 0xE5
// MAX44009 registers
#define MAX44009_LUX_HIGH_BYTE 0x03
#define MAX44009_LUX_LOW_BYTE 0x04
// Constructor
Sensors::Sensors() {}
// Initializes the I2C interface
void Sensors::begin() {
    Wire.begin();
}
// Reads temperature in Celsius from the SHT21 sensor
float Sensors::readTemperature() {
    uint16_t rawData = readSHT21(SHT21_TEMP_HOLD);
    if (rawData == 0xFFFF) return NAN;  // Return NaN if read fails
    return -46.85 + (175.72 * rawData / 65536.0);
}
// Reads humidity in percentage from the SHT21 sensor
float Sensors::readHumidity() {
    uint16_t rawData = readSHT21(SHT21_HUMIDITY_HOLD);
    if (rawData == 0xFFFF) return NAN;  // Return NaN if read fails
    return -6.0 + (125.0 * rawData / 65536.0);
}

// Reads luminosity in lux from the MAX44009 sensor
float Sensors::readLuminosity() {
    Wire.beginTransmission(MAX44009_ADDRESS);
    Wire.write(MAX44009_LUX_HIGH_BYTE);
    if (Wire.endTransmission() != 0) return NAN;  // Return NaN if I2C transmission fails
    Wire.requestFrom(MAX44009_ADDRESS, 2);
    if (Wire.available() == 2) {
        uint8_t highByte = Wire.read();
        uint8_t lowByte = Wire.read();
        uint8_t exponent = (highByte >> 4) & 0x0F;
        uint8_t mantissa = ((highByte & 0x0F) << 4) | (lowByte & 0x0F);
        return mantissa * (1 << exponent) * 0.045;  // Calculate lux
    }
    return NAN;  // Return NaN if no data available
}

// Helper function to read data from the SHT21 sensor
uint16_t Sensors::readSHT21(uint8_t command) {
    Wire.beginTransmission(SHT21_ADDRESS);
    Wire.write(command);
    if (Wire.endTransmission() != 0) return 0xFFFF;  // Return 0xFFFF if I2C transmission fails
    delay(50);  // Wait for the measurement to complete
    Wire.requestFrom(SHT21_ADDRESS, 2);
    if (Wire.available() == 2) {
        uint16_t rawData = (Wire.read() << 8) | Wire.read();
        rawData &= ~0x0003;  // Clear the status bits
        return rawData;
    }
    return 0xFFFF;  // Return 0xFFFF if no data available
}

