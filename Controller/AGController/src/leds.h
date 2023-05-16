#include <FastLED.h>

class Leds
{
public:
// LED
#define NUM_LEDS 10
#define DATA_PIN 15
    CRGB leds[NUM_LEDS];

    void initLED() 
    {
        FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS); // GRB ordering is assumed
        FastLED.setBrightness(40);
    }

    void setLEDStrip(int colour, int start = 0, int end = 10)
    {
        for (int i = start; i < end; i++)
        {
            leds[i] = colour;
        }
        FastLED.show();
    }
};