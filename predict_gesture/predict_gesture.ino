#include <TensorFlowLite_ESP32.h>
#include <tensorflow/lite/experimental/micro/kernels/all_ops_resolver.h>
#include <tensorflow/lite/experimental/micro/micro_error_reporter.h>
#include <tensorflow/lite/experimental/micro/micro_interpreter.h>
#include <tensorflow/lite/schema/schema_generated.h>
#include <tensorflow/lite/version.h>

#include <Arduino.h>
#include <Esp.h>
#include <HardwareSerial.h>
#include <WiFi.h>
#include <WiFiUdp.h>

#include "MPU9250.h"
#include "UDPChannel.h"
#include "HRTimer.h"

#include "model.h"

const int SAMPLE_COUNT = 200;
const char* AP_SSID = "iCheng-choy";
const char* AP_PWD = "nopassword";

MPU9250 IMU(9, 8);
UDPChannel Channel;
HRTimer LoopTimer;

char SerialBuffer[50];

int conut = 0;
unsigned char sign = 0;
unsigned char counter = 0;

short IMUData[9];

const int accelerationThreshold_HIGH = 3.5; // 阈值为3.5倍重力
const float ACCELERATION_THRESHOLD = 3000;
int smooth_count = 0;
int record_count = 0;

float Samples[6][SAMPLE_COUNT];

const int record_num = 70;

tflite::MicroErrorReporter tflErrorReporter;
tflite::ops::micro::AllOpsResolver tflOpsResolver;

const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

constexpr int tensorArenaSize = 8 * 1024;
byte tensorArena[tensorArenaSize];

const char* GESTURES[] = {
    "punch",
    "flex"
};
#define NUM_GESTURES (sizeof(GESTURES) / sizeof(GESTURES[0]))

int dirty = 0;

void setup()
{
    Serial.begin(115200);
    Channel.ConnectAP(AP_SSID, AP_PWD);

    /*
  mySerial.begin(115200, SERIAL_8N1, 15, 21);
  delay(500);
  mySerial.write(0XA5); 
  mySerial.write(0X55);
  mySerial.write(0X57);    //初始化GY25Z,输出陀螺和欧拉角
  mySerial.write(0X51); 
  delay(100); 
  mySerial.write(0XA5); 
  mySerial.write(0X56);    //初始化GY25Z,连续输出模式
  mySerial.write(0X02);    //初始化GY25Z,连续输出模式
  mySerial.write(0XFD);
  delay(100);
  pixels.begin(); 
  pixels.clear(); //清除颜色
  pixels.show(); //打印
  pixels.setPixelColor(0, pixels.Color(0,0,0)); //调颜色
  pixels.show(); //打印
  */

    record_count = -1; //防止第一次数据的错误触发

    Serial.println("Loading Model");
    tflModel = tflite::GetModel(model);

    int ModelVersion = tflModel->version();

    sprintf(SerialBuffer, "Model Version: %d, TFLite Version: %d", ModelVersion, TFLITE_SCHEMA_VERSION);
    Serial.println(SerialBuffer);

    if (ModelVersion != TFLITE_SCHEMA_VERSION) {
        Serial.println("Model schema mismatch!");
        while (1)
            ;
    } else {
        Serial.println("Model Loaded!");
    }

    tflInterpreter = new tflite::MicroInterpreter(tflModel, tflOpsResolver, tensorArena, tensorArenaSize, &tflErrorReporter);
    tflInterpreter->AllocateTensors();
    tflInputTensor = tflInterpreter->input(0);
    tflOutputTensor = tflInterpreter->output(0);

    sprintf(SerialBuffer, "Input Size: %d[%d, %d], Outpu Size: %d[%d, %d]", tflInputTensor->dims->size, tflInputTensor->dims->data[0], tflInputTensor->dims->data[1], tflOutputTensor->dims->size, tflOutputTensor->dims->data[0], tflOutputTensor->dims->data[1]);
    Serial.println(SerialBuffer);

    Serial.println("Starting IMU...");
    IMU.Init();
}

void loop()
{
    LoopTimer.Start();

    Acquisition();
    DetectMotion();

    while (dirty != 1) {

        //measure();
        //analysis();

        //Inference();


        //Serial.println(micros() - t);

        dirty = 1;
    }




/*
    float aSum = fabs(aX) + fabs(aY) + fabs(aZ);

    if (aSum >= accelerationThreshold_HIGH && record_count == -1) //动作开始
    {
        record_count = 0;
    }

    if (record_count < record_num && record_count != -1) //收集70个元组数据
    {
        record_count++;
    }

    if (record_count == record_num) //收集完成一次动作的70个元组数据
    {

        record_count = -1;
    }
*/

    auto t = LoopTimer.End();

    delay(10 - t / 1000);
}

bool DetectMotion()
{
    float sum = 0;

    for(int i = 0; i < 3; i++)
    {
        float a = (float)IMUData[i];
        sum += a * a;
    }

    Serial.println(sum);
    
    return sum > ACCELERATION_THRESHOLD;
}

void Acquisition()
{
    IMU.Read(IMUData);

    // sprintf(SerialBuffer, "%+5d\t%+5d\t%+5d | %+5d\t%+5d\t%+5d | %+5d\t%+5d\t%+5d\r\n", IMUData[0], IMUData[1], IMUData[2], IMUData[3], IMUData[4], IMUData[5], IMUData[6], IMUData[7], IMUData[8]);
    // Serial.print(SerialBuffer);

    Channel.Send((unsigned char*)IMUData, 18);  
}

void Inference()
{
    for (int k = 0; k < SAMPLE_COUNT; k++) {
      for(int i = 0; i < 6; i++)
      {
        tflInputTensor->data.f[k * 6 + i] = Samples[i][k];
      }
    }

    TfLiteStatus invokeStatus = tflInterpreter->Invoke();
    if (invokeStatus != kTfLiteOk) {
        Serial.println("Invoke failed!");
        while (1)
            ;
        return;
    }
    for (int i = 0; i < NUM_GESTURES; i++) {
        Serial.print(GESTURES[i]);
        Serial.print(": ");
        Serial.println(tflOutputTensor->data.f[i], 6);
    }
}
