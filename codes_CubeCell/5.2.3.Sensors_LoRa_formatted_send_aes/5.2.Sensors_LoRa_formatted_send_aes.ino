#include <Wire.h>
#include "LoRaWan_APP.h"      // CubeCell LoRa library
#include "Sensors.h"          // Predefined library for SHT21 and MAX44009
#include "aes.h"
aes_context ctx[2]; 
// Define the Vext pin to control sensor power
//#define Vext 21
// Declare RadioEvents structure
RadioEvents_t RadioEvents;
// Create an instance of the Sensors library
Sensors mySensors;
// Define the packet structure using a union for byte alignment
union DataPacket {
    struct {
        int channelNumber;               // 4 bytes for the channel number (integer)
        char writeKey[16];               // 16 bytes for write key (char array)
        float temperature;               // 4 bytes for temperature
        float humidity;                  // 4 bytes for humidity
        float luminosity;                // 4 bytes for luminosity
    } data;
    uint8_t bytes[32],cry_bytes[32];     // Total 32 bytes array view - added cry_bytes for encrypted frame
} packet;

// Function prototypes

void onTxDone(void);
void onTxTimeout(void);

void setup() {
    // Initialize serial communication for debugging
    Serial.begin(9600);
    aes_set_key((uint8_t*)"smartcomputerlab",16,ctx);
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
    Radio.SetChannel(868000000);  // Example frequency for EU 868 MHz
    Radio.SetTxConfig(MODEM_LORA, 14, 0, 0, 7, 1, 8, false, true, 0, 0, false, 3000);
    // Initialize packet data
    packet.data.channelNumber = 1;                 // Example channel number
    strncpy(packet.data.writeKey, "1234567890ABCDEF", 16); // 16-character write key
    Serial.println("Sensor and LoRa setup complete.");
}

void loop() {
    // Read sensor values
    packet.data.temperature = mySensors.readTemperature();
    packet.data.humidity = mySensors.readHumidity();
    packet.data.luminosity = mySensors.readLuminosity();
    // Print sensor values for debugging
    Serial.print("Temperature: ");
    Serial.print(packet.data.temperature);
    Serial.println(" °C");
    Serial.print("Humidity: ");
    Serial.print(packet.data.humidity);
    Serial.println(" %");
    Serial.print("Luminosity: ");
    Serial.print(packet.data.luminosity);
    Serial.println(" lux");
    aes_encrypt(packet.bytes, packet.cry_bytes, ctx ); 
    aes_encrypt(packet.bytes+16, packet.cry_bytes+16, ctx );
    // Send LoRa packet with payload
    Radio.Send(packet.bytes, sizeof(packet.cry_bytes));
    // Wait before sending the next packet
    delay(6000);  // Send every 60 seconds (adjust as needed)
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
