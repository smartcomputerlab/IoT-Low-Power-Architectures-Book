#include <Wire.h>
#include "LoRaWan_APP.h"      // CubeCell LoRa library
#include "Sensors.h"          // Predefined library for SHT21 and MAX44009
// Define the Vext pin to control sensor power
// #define Vext 21
// Declare RadioEvents structure
RadioEvents_t RadioEvents;
// Create an instance of the Sensors library
Sensors mySensors;
// Unions to convert float values into byte arrays
union FloatToBytes {
    float value;
    uint8_t bytes[4];
};
// Create unions for each sensor reading
FloatToBytes temperatureData;
FloatToBytes humidityData;
FloatToBytes luminosityData;

// LoRa payload array
uint8_t payload[12];  // 3 floats x 4 bytes each

// Function prototypes
void onTxDone(void);
void onTxTimeout(void);

void setup() {
    // Initialize serial communication for debugging
    Serial.begin(9600);
    // Initialize the Sensors library
    pinMode(Vext, OUTPUT);
    digitalWrite(Vext, LOW);   // Power on sensors by setting Vext to LOW
    delay(10);                 // Wait for sensors to power up
    mySensors.begin();         // Initialize I2C and sensors
    // Initialize LoRa and set RadioEvents callbacks
    RadioEvents.TxDone = onTxDone;
    RadioEvents.TxTimeout = onTxTimeout;
    Radio.Init(&RadioEvents);
    // Set default LoRa parameters (frequency, power, etc.)
    Radio.SetChannel(868100000);  // Example frequency for EU 868 MHz
    Radio.SetTxConfig(MODEM_LORA, 14, 0, 0, 7, 1, 8, false, true, 0, 0, false, 3000);
    Serial.println("Sensor and LoRa setup complete.");
}

void loop() {
    // Read sensor values
    temperatureData.value = mySensors.readTemperature();
    humidityData.value = mySensors.readHumidity();
    luminosityData.value = mySensors.readLuminosity();
    // Print sensor values for debugging
    Serial.print("Temperature: ");
    Serial.print(temperatureData.value);
    Serial.println(" °C");
    Serial.print("Humidity: ");
    Serial.print(humidityData.value);
    Serial.println(" %");
    Serial.print("Luminosity: ");
    Serial.print(luminosityData.value);
    Serial.println(" lux");
    // Pack sensor data into payload
    for (int i = 0; i < 4; i++) {
        payload[i] = temperatureData.bytes[i];
        payload[i + 4] = humidityData.bytes[i];
        payload[i + 8] = luminosityData.bytes[i];
    }
    // Send LoRa packet
    Radio.Send(payload, sizeof(payload));
    // Wait before sending the next packet
        delay(6000);  // Send every 6 seconds (adjust as needed)
}
// Callback function called when LoRa transmission is done
void onTxDone(void) {
    Serial.println("LoRa transmission successful!");
    Radio.Sleep();  // Put the LoRa radio back to sleep after transmission
}
// Callback function called when LoRa transmission times out
void onTxTimeout(void) {
    Serial.println("LoRa transmission timed out!");
    Radio.Sleep();  // Put the LoRa radio back to sleep after a timeout
}
