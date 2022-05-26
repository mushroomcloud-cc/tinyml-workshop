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
#include "LED.h"

#include "model.h"

const int BUTTOM_PIN = 4;

const char* AP_SSID = "iCheng";
const char* AP_PWD = "nopassword";

const char* GESTURES[] = {
    "cross",
    "circle"
};
const int NUM_GESTURES = sizeof(GESTURES) / sizeof(GESTURES[0]);
const int SAMPLE_COUNT = 120;

MPU9250 IMU(9, 8);
UDPChannel Channel;
HRTimer LoopTimer;
HRTimer ExeTimer;

char SerialBuffer[50];

int conut = 0;
unsigned char sign = 0;
unsigned char counter = 0;

short SampleData[9];
int IMUData[9];
int LastData[9];

const float ACCELERATION_THRESHOLD = 2E6;
const int SMOTH_COUNT = 5;
int RecordCount = 0;

float Samples[6][SAMPLE_COUNT];

tflite::MicroErrorReporter tflErrorReporter;
tflite::ops::micro::AllOpsResolver tflOpsResolver;

const tflite::Model* tflModel = nullptr;
tflite::MicroInterpreter* tflInterpreter = nullptr;
TfLiteTensor* tflInputTensor = nullptr;
TfLiteTensor* tflOutputTensor = nullptr;

constexpr int tensorArenaSize = 8 * 1024;
byte tensorArena[tensorArenaSize];

void setup()
{
    pinMode(BUTTOM_PIN, INPUT_PULLUP);
 
    Serial.begin(115200);
    Channel.ConnectAP(AP_SSID, AP_PWD);

    RecordCount = -1; // 待采样

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

    // TrainingMode();
    PredictMode();

    auto t = LoopTimer.End() / 1000.0;
    // Serial.println(t);

    if(t < 10) 
    {
      delay(10 - t); 
    }
}

//
// Functions
//


void TrainingMode()
{
    Acquisition();

    if(digitalRead(BUTTOM_PIN) == LOW && RecordCount == -1)
    {
        RecordCount = 0;
        Led.On();
    }

    if(RecordCount > -1)
    {
        RecordCount++;        
        Send();         
    }
      
    if(RecordCount >= SAMPLE_COUNT)
    {
        RecordCount = -1;        
        Led.Off();
    } 
}

void PredictMode()
{
    Acquisition();
   
    if((digitalRead(BUTTOM_PIN) == LOW) && RecordCount == -1)
    // if(DetectMotion() && RecordCount == -1)
    {
        RecordCount = 0;
        Led.On();
    }

    if(RecordCount >= SAMPLE_COUNT)
    {
        RecordCount = -1;        
        Led.Off();
        
        if(Inference()) Result();
    } 
    else if(RecordCount > -1)
    {
        for(int i = 0; i < 9; i++)
        {
            Samples[i][RecordCount] = IMUData[i] / 32768.0;    
        }
      
        RecordCount++;        
    }  
}


bool DetectMotion()
{
    float sum = 0;

    for(int i = 3; i < 6; i++)
    {
        float a = (float)IMUData[i] - (float)LastData[i];
        sum += a * a;
    }

    for(int i = 0; i < 9; i++)
    {
        LastData[i] = IMUData[i];
    }

    bool ret = sum > ACCELERATION_THRESHOLD;
    // if(ret) Serial.println(sum);
    
    return ret;
}

void Acquisition()
{
    for(int i = 0; i < 9; i++)
    {
        IMUData[i] = 0;      
    }

    for(int c = 0; c < SMOTH_COUNT; c++)
    {
        IMU.Read(SampleData);
        
        for(int i = 0; i < 9; i++)
        {
            IMUData[i] += SampleData[i];      
        }
    }

    // sprintf(SerialBuffer, "%+5d\t%+5d\t%+5d | %+5d\t%+5d\t%+5d | %+5d\t%+5d\t%+5d\r\n", IMUData[0], IMUData[1], IMUData[2], IMUData[3], IMUData[4], IMUData[5], IMUData[6], IMUData[7], IMUData[8]);
    // Serial.print(SerialBuffer);
}

void Send()
{
    Channel.Send(RecordCount, (unsigned char*)IMUData, 36);  
}

bool Inference()
{
    bool ret = false;
  
    for (int k = 0; k < SAMPLE_COUNT; k++) {
      for(int i = 0; i < 6; i++)
      {
        tflInputTensor->data.f[k * 6 + i] = Samples[i][k];
      }
    }

    ExeTimer.Start();
    TfLiteStatus invokeStatus = tflInterpreter->Invoke();
    unsigned long t = ExeTimer.End();
    
    if (invokeStatus == kTfLiteOk) 
    {
      sprintf(SerialBuffer, "Invoke In %8.6f(ms)", t / 1000.0);
      Serial.println(SerialBuffer);

      ret = true;
    }
    else
    {
        Serial.println("Invoke failed!");
    }

    return ret;
}

void Result()
{
    float p_threshold = 0.99;
  
    auto p_cross = tflOutputTensor->data.f[0];
    auto p_circle = tflOutputTensor->data.f[1];

    sprintf(SerialBuffer, "Cross: %8.6f, Circle: %8.6f", p_cross, p_circle);
    Serial.println(SerialBuffer);

    if(p_cross > p_threshold)
    { 
        Led.Red();
    }
    else if(p_circle > p_threshold)
    {
        Led.Blue();
    }
    else
    {
        Led.Blank();
    
    }  
}

void ShowOutput()
{
    for (int i = 0; i < NUM_GESTURES; i++) 
    {
      sprintf(SerialBuffer, "%s: %8.6f", GESTURES[i], tflOutputTensor->data.f[i]);
      Serial.println(SerialBuffer);
    }
}
