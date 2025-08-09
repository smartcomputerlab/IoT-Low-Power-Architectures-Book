typedef union 
{
  uint8_t frame[16]; // frame with bytes
..char name[16];     // character string
}

pack_t sdp;  // packet to send

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
}

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

void loop()
{ 
    if(lora_idle==true)
    {
      delay(100);
      lora_idle = false;    // will be set by OnTxDone or OnTxTimeout
      memcpy(sdp.name,”smartcomputerlab”,16)
      delay(300);
      Radio.Send((uint8_t *)sdp.frame,32); //send the package out 
    }
}

