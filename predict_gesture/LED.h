#ifndef _LED_H_
#define _LED_H_

const int LED_PIN = 10;

class LED {
public:
    LED(int pin);
    void On();
    void Off();
    void Toggle();

private:
    int Pin;
    bool State;
};

extern LED Led;

#endif // _LED_H_
