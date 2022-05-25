#include "MPU9250.h"

#include <Arduino.h>
#include <Wire.h>

#define GET_RINT(p, i) (short)(((unsigned short)p[i]) << 8 | p[i + 1]);
#define GET_INT(p, i) (short)(((unsigned short)p[i + 1]) << 8 | p[i]);

MPU9250::MPU9250(int scl, int sda)
{
    if(scl >= 0 && sda >= 0)
    {
      if(!Wire.setPins(sda, scl)) Serial.println("Wire Set Pin Faild!");
    }
    
    if(!Wire.begin()) Serial.println("Wire Begin Faild!");
}

void MPU9250::Read(short* data)
{
    unsigned char buff[25];

    // Read accelerometer and gyroscope
    I2Cread(MPU9250_ADDRESS, ACCEL_XOUT_H, 14, buff);

    unsigned char ST1;
    // Read register Status 1 and wait for the DRDY: Data Ready
    // I2Cread(AK8963_ADDRESS, AK8963_ST1, 1, &ST1);
    // if (ST1 & 0x01) 
    {
        // Read magnetometer data
        // I2Cread(AK8963_ADDRESS, AK8963_XOUT_L, 6, buff + 14);
    }

    // ax, ay, az
    data[0] = GET_RINT(buff, 0);
    data[1] = GET_RINT(buff, 2);
    data[2] = GET_RINT(buff, 4);

    // Gyroscope
    data[3] = GET_RINT(buff, 8);
    data[4] = GET_RINT(buff, 10);
    data[5] = GET_RINT(buff, 12);

    // mx, my, mz
    data[6] = GET_INT(buff, 14);
    data[7] = GET_INT(buff, 16);;
    data[8] = GET_INT(buff, 18);
}

void MPU9250::Init()
{ 
  I2CwriteByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x80);  // Reset mpu9250
  I2CwriteByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x01);  // Set clock of mpu9250

  I2CwriteByte(MPU9250_ADDRESS, CONFIG, LPF_BANDWIDTH_FULL);   // Set accelerometers low pass filter at 5Hz
  I2CwriteByte(MPU9250_ADDRESS, ACCEL_CONFIG2, LPF_BANDWIDTH_FULL);   // Set gyroscope low pass filter at 5Hz
  I2CwriteByte(MPU9250_ADDRESS, GYRO_CONFIG, GYRO_FULL_SCALE_250_DPS);  // Configure gyroscope range
  I2CwriteByte(MPU9250_ADDRESS, ACCEL_CONFIG, ACC_FULL_SCALE_2_G);  // Configure accelerometers range
  I2CwriteByte(MPU9250_ADDRESS, INT_PIN_CFG, 0x02);  // Set by pass mode for the magnetometers

  I2CwriteByte(AK8963_ADDRESS, AK8963_ASTC, 0x01);  // Reset magnetometer
  I2CwriteByte(AK8963_ADDRESS, AK8963_CNTL, 0x00);  // Set magnetometer power down
  delay(1);
  I2CwriteByte(AK8963_ADDRESS, AK8963_CNTL, 0x16);  // Request continuous magnetometer measurements in 16 bits

  unsigned char ID_MPU9250;
  unsigned char ID_AK8963;
  char buf[50];
  I2Cread(MPU9250_ADDRESS, WHO_AM_I_MPU9250, 1, &ID_MPU9250);
  I2Cread(MPU9250_ADDRESS, WHO_AM_I_AK8963, 1, &ID_AK8963);
  sprintf(buf, "IMU ID: %02x, Mag ID: %02x", ID_MPU9250, ID_AK8963);  
  Serial.println(buf);
}

// This function read Nbytes bytes from I2C device at address Address.
// Put read bytes starting at register Register in the Data array.
void MPU9250::I2Cread(int Address, int Register, int Nbytes, unsigned char* Data)
{
    // Set register address
    Wire.beginTransmission(Address);
    Wire.write(Register);
    Wire.endTransmission();

    // Read Nbytes
    Wire.requestFrom(Address, Nbytes);
    uint8_t index = 0;
    while (Wire.available()) 
    {
        Data[index++] = Wire.read();
    }
}

// Write a byte (Data) in device (Address) at register (Register)
void MPU9250::I2CwriteByte(int Address, int Register, unsigned char Data)
{
    // Set register address
    Wire.beginTransmission(Address);
    Wire.write(Register);
    Wire.write(Data);
    Wire.endTransmission();
}
