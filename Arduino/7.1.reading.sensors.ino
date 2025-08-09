#include <SHT21.h>  // include SHT21 library
#include <Max44009.h>
Max44009 myLux(0x4A);
SHT21 sht; 

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

float lumi=100.0, temp=24.0, humi=23.0;

void loop()
{ 
      sensors(&lumi,&temp,&humi);
      Serial.println(lumi);Serial.println(temp);Serial.println(humi);
      delay(300);
}

