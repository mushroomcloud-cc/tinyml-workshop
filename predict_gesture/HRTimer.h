#ifndef _HRTIMER_H_
#define _HRTIMER_H_

#include "MPU9250_Reg.h"

class HRTimer {
public:
    HRTimer();
    void Start();
    unsigned long End();

private:
    unsigned long LastTime;
};

#endif // _HRTIMER_H_