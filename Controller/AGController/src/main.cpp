#include <Arduino.h>
#include <M5Stack.h>

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Lcd.setTextColor(0xE4DFDA);
	M5.Lcd.setTextSize(3);

	M5.Lcd.drawString("Hello Goat-inator", (int)(M5.Lcd.width()/2), (int)(M5.Lcd.height()/2), 2);
}

void loop()
{
	// put your main code here, to run repeatedly:
	M5.update();
	if (M5.BtnA.wasPressed())
	{
		M5.Lcd.clear();
		M5.Lcd.println("Goat World-inator");
	}
}