#include <Wire.h>
#include "LoRaWan_APP.h"      // CubeCell LoRa library
#include "Sensors.h"          // Predefined library for SHT21 and MAX44009
#include "Arduino.h"          // For sleep functions
#include "aes.h"
aes_context ctx[2];           // AES encryption type context
static int scycle=10,skpack=40;
static float stemp=20.0, sdelta=0.2;
bool ackReceived = false;                              
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
    uint8_t bytes[32];                   // Total 32 bytes array view
} data_packet;

union AckPacket {
    struct {
        int channelNumber;               // 4 bytes for the channel number (integer)
        int cycle;               // 4 bytes for temperature
        float delta;                  // 4 bytes for humidity
        int luminosity;                // 4 bytes for luminosity
    } ack;
    uint8_t bytes[16];                   // Total 32 bytes array view
} ack_packet;

// Timer for low power mode
TimerEvent_t sleepTimer;
bool sleepTimerExpired;  // Records whether our sleep/low power timer expired
// Function prototypes
void onTxDone(void);
void onTxTimeout(void);
void lowPowerSleep(uint32_t sleeptime);
static void wakeUp();

void aes_encrypt(uint8_t *data, uint8_t *encryptedData)    // prepared to encrypt 2*16 bytes
{
    aes_encrypt(data, encryptedData, ctx ); 
    aes_encrypt(data+16, encryptedData+16, ctx ); 
}

void aes_decrypt(uint8_t *data, uint8_t *decryptedData)    // prepared to encrypt 2*16 bytes
{
    aes_decrypt(data,decryptedData, ctx );  
}
// Function to enter low power sleep for a specified duration
static void LowPowerSleep(uint32_t sleeptime) {
    sleepTimerExpired = false;
    TimerInit(&sleepTimer, &wakeUp);
        TimerSetValue(&sleepTimer, sleeptime);
    TimerStart(&sleepTimer);
    while (!sleepTimerExpired) {
        lowPowerHandler();
    }
    TimerStop(&sleepTimer);
}

void setup() {
    // Initialize serial communication for debugging
    Serial.begin(9600);
    // Initialize the Sensors library
    pinMode(Vext, OUTPUT);
    digitalWrite(Vext, LOW);   // Power on sensors by setting Vext to LOW
    delay(10);                 // Wait for sensors to power up
    mySensors.begin();         // Initialize I2C and sensors
    aes_set_key((uint8_t*)"smartcomputerlab",16,ctx);delay(300);
    // Initialize LoRa and set RadioEvents callbacks
    RadioEvents.TxDone = onTxDone;
    RadioEvents.TxTimeout = onTxTimeout;
    RadioEvents.RxDone = OnRxDone;
    RadioEvents.RxTimeout = OnRxTimeout;
    Radio.Init(&RadioEvents);
    // Set default LoRa parameters (frequency, power, etc.)
    Radio.SetChannel(868000000);  // Example frequency for EU 868 MHz
    Radio.SetTxConfig(MODEM_LORA, 14, 0, 0, 7, 1, 8, false, true, 0, 0, false, 3000);
    Radio.SetRxConfig(MODEM_LORA, 0, 7, 1, 0, 8, 0, false, 0, true, 0, 0, false, true);
    // Initialize packet data
    data_packet.data.channelNumber = 1;                 // Example channel number
    strncpy(data_packet.data.writeKey, "1234567890ABCDEF", 16); // 16-character write key
    Serial.println("Sensor and LoRa setup complete.");
}

void loop() {
    delay(50);
    pinMode(Vext, OUTPUT);
    digitalWrite(Vext, LOW); 
    delay(100);
    mySensors.begin(); delay(100);
    data_packet.data.temperature = mySensors.readTemperature();
    data_packet.data.humidity = mySensors.readHumidity();
    data_packet.data.luminosity = mySensors.readLuminosity();
    strncpy(data_packet.data.writeKey,"smartcomputerlab",16);
    // Print sensor values for debugging
    delay(100); // Allow time for transmission before sleeping
    Serial.print("Temperature: ");
    Serial.print(data_packet.data.temperature);
    Serial.println(" °C");
    Serial.print("Humidity: ");
    Serial.print(data_packet.data.humidity);
    Serial.println(" %");
    Serial.print("Luminosity: ");
    Serial.print(data_packet.data.luminosity);
    Serial.println(" lux");
    delay(100);
    if(abs(data_packet.data.temperature-stemp)>sdelta)
      {
     // Encrypt the packet data
      uint8_t encryptedData[32];
      aes_encrypt(data_packet.bytes, encryptedData);
      // Send LoRa packet with encrypted payload
      Radio.Send(encryptedData, sizeof(encryptedData));
      // Enter low power mode until the next transmission
      stemp=data_packet.data.temperature;
      }
    pinMode(Vext, OUTPUT);
    digitalWrite(Vext, HIGH);   // Power on sensors by setting Vext to LOW  
    Wire.end();
    LowPowerSleep(10000);       // Enter low power sleep for 10 seconds
}
// Function to handle reception of packets
void OnRxDone(uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr) {
    Serial.print("Packet received: cycle:");
    aes_decrypt(payload, ack_packet.bytes);
       Serial.println(ack_packet.ack.cycle); scycle=ack_packet.ack.cycle;
    delay(10);
    Radio.Sleep(); // Put radio to sleep after reception
}
// Callback function called when LoRa transmission is done
void onTxDone(void) {
    Serial.println("Packet sent");
    delay(10);
    ackReceived = false;
    Radio.Rx(2000); // Wait for ACK with a timeout of 2000 ms
}
// Function to handle reception timeout
void OnRxTimeout(void) {
    Serial.println("ACK not received (Timeout).");
    Radio.Sleep();
}
// Callback function called when LoRa transmission times out
void onTxTimeout(void) {
    Serial.println("LoRa transmission timed out!");
    Radio.Sleep();  // Put the LoRa radio back to sleep after a timeout
}
// Timer wakeup function to end low power sleep
static void wakeUp() {
    sleepTimerExpired = true;
}
