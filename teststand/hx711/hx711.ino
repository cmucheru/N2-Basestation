#include <Arduino.h>
#include "HX711.h"
const int DT_PIN = 2;
const int SCK_PIN = 3;
HX711 scale;

void setup() {
  Serial.begin(9600);
  Serial.println("start");
  scale.begin(DT_PIN, SCK_PIN);

  Serial.print("read:");
  Serial.println(scale.read());

  scale.set_scale();
  scale.tare();

  Serial.print("load reference weight");
  for (int i=0;i<5;i++){
    Serial.print(".");
    delay(1000);    
  }
  Serial.println();
  
  float unit=scale.get_units(10);
  Serial.println(unit);

  Serial.print("remove reference weight");
  for (int i=0;i<5;i++){
    Serial.print(".");
    delay(1000);    
  }
  Serial.println();

  Serial.print("input reference weight [g]: ");
  while(Serial.available() == 0) {} 
  float reference_i= Serial.readStringUntil('\n').toFloat();
  Serial.println(reference_i);
  scale.set_scale(unit/reference_i);
  scale.tare();

  float deviation = scale.get_units(10);

  Serial.print("offset: ");
  Serial.println(deviation);
//  scale.set_offset(deviation); //definition of offset?

  Serial.print("read (calibrated):");
  Serial.println(scale.get_units(10));
}


void loop() {
  Serial.println(scale.get_units(1), 1);
}