/*
 Note: The MPU9250 is an I2C sensor and uses the Arduino Wire library.
 Because the sensor is not 5V tolerant, we are using a 3.3 V 8 MHz Pro Mini or
 a 3.3 V Teensy 3.1. We have disabled the internal pull-ups used by the Wire
 library in the Wire.h/twi.c utility file. We are also using the 400 kHz fast
 I2C mode by setting the TWI_FREQ  to 400000L /twi.h utility file.
 */
#ifndef _MPU9250_H_
#define _MPU9250_H_

#include "MPU9250_Reg.h"

class MPU9250 {
public:
    MPU9250(int scl, int sda);
    void Init();
    void Read(short* buff);

private:
    // This function read Nbytes bytes from I2C device at address Address.
    // Put read bytes starting at register Register in the Data array.
    void I2Cread(int Address, int Register, int Nbytes, unsigned char* Data);
    // Write a byte (Data) in device (Address) at register (Register)
    void I2CwriteByte(int Address, int Register, unsigned char Data);
};

#endif // _MPU9250_H_
