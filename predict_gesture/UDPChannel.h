#ifndef _UDP_CHANNEL_H
#define _UDP_CHANNEL_H

#include <WiFiUdp.h>

class UDPChannel
{
public:
  UDPChannel();

  void ConnectAP(const char* ssid, const char* pwd);
  void Send(int count, unsigned char* buf, int len);
  
private:
  WiFiUDP UDP;
};

#endif
