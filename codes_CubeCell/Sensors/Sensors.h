#ifndef SENSORS_H
#define SENSORS_H
#include <Arduino.h>
#include <Wire.h>
// I2C addresses for the sensors
#define SHT21_ADDRESS 0x40
#define MAX44009_ADDRESS 0x4A

class Sensors {
public:
    // Constructor
    Sensors();
    // Initialization method
    void begin();
    // Methods to read sensor data
    float readTemperature();
    float readHumidity();
    float readLuminosity();

private:
    // Private helper functions for SHT21
    uint16_t readSHT21(uint8_t command);
};

#endif // SENSORS_H

