#include "LED.h"

#include <Arduino.h>

LED::LED(int pin)
{
    this->Pin = pin;
    pinMode(this->Pin, OUTPUT);
      
    this->Off();
}

void LED::On()
{
    digitalWrite(LED_PIN, HIGH);
    this->State = true;
}

void LED::Off()
{
    digitalWrite(LED_PIN, LOW);
    this->State = true;
}
    
void LED::Toggle()
{
    this->State ? this->Off() : this->On();
}

LED Led(LED_PIN);
