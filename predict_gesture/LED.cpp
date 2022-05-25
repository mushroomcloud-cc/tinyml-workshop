#include "LED.h"

#include <Arduino.h>

LED::LED()
{
    pinMode(LED_PIN, OUTPUT);
    pinMode(BLUE_PIN, OUTPUT);
    pinMode(RED_PIN, OUTPUT);
              
    this->Off();
    this->Blank();
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

void LED::Blue()
{
    digitalWrite(RED_PIN, HIGH);
    digitalWrite(BLUE_PIN, LOW);
}

void LED::Red()
{
    digitalWrite(BLUE_PIN, HIGH);
    digitalWrite(RED_PIN, LOW);
}

void LED::Blank()
{
    digitalWrite(BLUE_PIN, HIGH);
    digitalWrite(RED_PIN, HIGH);  
}

LED Led;
