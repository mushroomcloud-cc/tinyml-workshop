#include "HRTimer.h"

#include <Arduino.h>

HRTimer::HRTimer()
{
    this->LastTime = 0;
}

void HRTimer::Start()
{
    this->LastTime = micros();
}


unsigned long HRTimer::End()
{
    unsigned long ret; 
    unsigned long t = micros();
    
    ret = t - this->LastTime;
    if(t < this->LastTime)
    {
        ret = (unsigned long)-1 - ret + 1;
    }

    return ret;
}
