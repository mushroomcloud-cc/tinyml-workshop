#include "UDPChannel.h"

#include "LED.h"
#include <WiFi.h>


UDPChannel::UDPChannel()
{
  
}

void UDPChannel::ConnectAP(const char* ssid, const char* pwd)
{
    // WiFi.softAP(AP_SSID, AP_PWD);
    WiFi.begin(ssid, pwd);

    Serial.write("Waiting for connect to AP");
    while (!WiFi.isConnected())
    {
        Led.Toggle();
        Serial.write('.');
    }

    Led.Off();
    Serial.println("");
}
  
void UDPChannel::Send(unsigned char* buf, int len)
{
    UDP.beginPacket("255.255.255.255", 8000);
    UDP.write(buf, len);
    UDP.endPacket();
}
