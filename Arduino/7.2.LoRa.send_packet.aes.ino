#include "LoRaWan_APP.h"
#include "Arduino.h"
#include "aes.h"
#include <SHT21.h>  // include SHT21 library
#include <Max44009.h>
Max44009 myLux(0x4A);
SHT21 sht; 
aes_context ctx[2];
const uint8_t key[16] = {115,109,97,114,116,99,111,109,112,117,116,101,114,108,97,98};
// "smartcomputerlab"
#define RF_FREQUENCY                                868000000 // Hz
#define TX_OUTPUT_POWER                             14        // dBm
#define LORA_BANDWIDTH                              0         // [0: 125 kHz,
                                                              //  1: 250 kHz,
                                                              //  2: 500 kHz,
                                                              //  3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5,
                                                              //  2: 4/6,
                                                              //  3: 4/7,
                                                              //  4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false
#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 30 // Define the payload size here

char txpacket[BUFFER_SIZE];
char rxpacket[BUFFER_SIZE];

static RadioEvents_t RadioEvents;
float txNumber;

typedef union 
{
 uint8_t frame[36]; // frames with bytes
 struct
   {
   int    channel;
   char   wkey[16];
   float  sensor[3];    
   uint32_t pad;
   } pay;
} pack_t;

pack_t sdp, cry_sdp;  // clear and encrypted packets

//Some utilities for going into low power mode
TimerEvent_t sleepTimer;
//Records whether our sleep/low power timer expired
bool sleepTimerExpired;

static void wakeUp()
{
  sleepTimerExpired=true;
}
static void lowPowerSleep(uint32_t sleeptime)
{
  sleepTimerExpired=false;
  TimerInit( &sleepTimer, &wakeUp );
  TimerSetValue( &sleepTimer, sleeptime );
  TimerStart( &sleepTimer );
  //Low power handler also gets interrupted by other timers
  //So wait until our timer had expired
  while (!sleepTimerExpired) lowPowerHandler();
  TimerStop( &sleepTimer );
}

void sensors(float *l,float *t,float *h)
{
  pinMode(Vext,OUTPUT); delay(100);
  digitalWrite(Vext,LOW);//set vext to high
  delay(100);
  Wire.begin();  delay(100); 
  Serial.begin(9600); // begin Serial
  myLux.setContinuousMode();
  *t = sht.getTemperature();  // get temp from SHT 
  *h = sht.getHumidity(); // get temp from SHT
  *l = myLux.getLux();
  digitalWrite(Vext,HIGH);delay(100);
  Wire.end();
}

void setup(){
  Serial.begin(9600);delay(300);
  txNumber=0;
  RadioEvents.TxDone = OnTxDone;
  RadioEvents.TxTimeout = OnTxTimeout;
  Radio.Init( &RadioEvents );
  Radio.SetChannel( RF_FREQUENCY );
  Radio.SetTxConfig( MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                                   LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                                   LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                                   true, 0, 0, LORA_IQ_INVERSION_ON, 3000 ); 

  aes_set_key(key,
                 16,         // len in bytes - length_type
                ctx );    
}

bool lora_idle=true;

void OnTxDone( void )
{
  Radio.Sleep( );
  Serial.println("TX done......");
  lora_idle=true;
  delay(100);
}

void OnTxTimeout( void )
{
  Radio.Sleep( );
  Serial.println("TX Timeout......");
  lora_idle = true;
}

float lumi=100.0, temp=24.0, humi=23.0;

int ttsleep=4000;

void loop()
{ 
    lowPowerSleep(ttsleep);  
    if(lora_idle==true)
    {      delay(100);
      lora_idle = false;    // will be set by OnTxDone or OnTxTimeout
      sensors(&lumi,&temp,&humi);
      sdp.pay.channel=1234; strncpy(sdp.pay.wkey,"smartcomputerlab",16);
      sdp.pay.sensor[0]=lumi;sdp.pay.sensor[1]=temp;sdp.pay.sensor[2]=humi;
      Serial.println(lumi);Serial.println(temp);Serial.println(humi);
      aes_encrypt(sdp.frame,cry_sdp.frame,ctx); 
      delay(200);
      aes_encrypt(sdp.frame+16,cry_sdp.frame+16,ctx); 
      delay(300);
      Radio.Send((uint8_t *)cry_sdp.frame,32); //send the package out 
    }
}

