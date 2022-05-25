#ifndef _LED_H_
#define _LED_H_

const int LED_PIN = 10;
const int BLUE_PIN = 6;
const int RED_PIN = 7;

class LED {
public:
    LED();
    
    void On();
    void Off();
    void Toggle();

    void Blue();
    void Red();
    void Blank();
private:
    bool State;
};

extern LED Led;

#endif // _LED_H_
