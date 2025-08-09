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
#define LORA_SPREADING_FACTOR                       8         // [SF7..SF12]
#define LORA_CODINGRATE                             4         // [1: 4/5,
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
 uint8_t frame[36];  
 struct
   {
   int    channel;
   char   wkey[16];
   float  sensor[3];    
   uint32_t pad;
   } pay;
} pack_t;
pack_t sdp, cry_sdp;   

typedef union 
{
 uint8_t frame[20];   
 struct
   {
   int    channel;
   float  sensor[3];   
   uint32_t pad;
   } pay;
} urgpack_t;
urgpack_t urgp, cry_urgp;

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

uint16_t read_Bat()
{
  uint16_t v;
  delay(40);
  pinMode(VBAT_ADC_CTL,OUTPUT);
  digitalWrite(VBAT_ADC_CTL,LOW);
  v=analogRead(ADC)+550; //*2;
  pinMode(VBAT_ADC_CTL, INPUT);
  return v;
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

  aes_set_key(key, 16, ctx );   // 16 - len in bytes - length_type 
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
float vbat=0.0;
const float tbat=3000;  // mV
static float sdelta=0.04, stemp=20.0;
static int npos=0, nneg=0;
const float thigh=30.0, tlow=15.0;
const float lhigh=3000.0, llow=10.0;
static int ncycle=1, cmax=64;
static float dmin=0.01,dmax=0.4;
int ttsleep=1000;

void loop()
{ 
    lowPowerSleep(ttsleep*ncycle);  
    if(lora_idle==true)
    {
      delay(100);
      lora_idle = false;    // will be set by OnTxDone or OnTxTimeout
      sensors(&lumi,&temp,&humi);
      Serial.println(lumi);Serial.println(temp);Serial.println(humi);
      vbat = (float)read_Bat();
      Serial.println(vbat);
      if (temp>thigh || temp<tlow || vbat<tbat || lumi>lhigh || lumi<llow) 
      {
        Serial.println("Urgent packet sent");
        ncycle=1; npos=0; nneg=0;
        sdelta=dmin;
        sdp.pay.channel=1234;
        urgp.pay.sensor[0]=lumi;urgp.pay.sensor[1]=temp;urgp.pay.sensor[2]=vbat;
        Serial.println(lumi);Serial.println(temp);Serial.println(humi);
        aes_encrypt(urgp.frame,cry_urgp.frame,ctx); 
        delay(300);
        Radio.Send((uint8_t *)cry_urgp.frame,16); //send the package out 
        delay(300);
      }
      else if (abs(stemp-temp)>sdelta||(thigh-temp)<sdelta||(temp-tlow)< sdelta) 
      {
      Serial.println("delta - Packet sent");   delay(200);
      stemp=temp;
      if (npos>0) 
        {
          if (ncycle > 2)  ncycle = ncycle/2.0;
          else if (sdelta < dmax)  sdelta += 0.1*sdelta; // Increase delta by 10%
        }
        npos++;nneg=0;
        sdp.pay.channel=1234; strncpy(sdp.pay.wkey,"smartcomputerlab",16);
        sdp.pay.sensor[0]=lumi;sdp.pay.sensor[1]=temp;sdp.pay.sensor[2]=humi;
        aes_encrypt(sdp.frame,cry_sdp.frame,ctx); 
        delay(200);
        aes_encrypt(sdp.frame+16,cry_sdp.frame+16,ctx); 
        delay(300);
        Radio.Send((uint8_t *)cry_sdp.frame,32); //send the package out 
        Serial.println("Packet sent");   delay(200);
      }
      else
      {
        Serial.println("Packet not sent");   delay(200);
        lora_idle=true;
        if (nneg> 0) 
        {
          if (ncycle<cmax) ncycle *= 2; // Double the cycle
          else if (sdelta > dmin) sdelta -= 0.1*sdelta; // Decrease delta by 10%
        }
        npos=0; nneg++; 
      } 
    }
}

