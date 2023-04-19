// Official libaries.
#include <Arduino.h>
#include <M5Stack.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>

#include <FastLED.h>

// Own Files.
#include "keyboard.h"
#include "numpad.h"

// Initate functions.
void motionSensor(void* param);
void connectToWifi(char *ssid, char *psw);
char *getWifiSSID();
String httpLogin();
char *getStorage();
void unlockDoor();
void setLEDStrip(int colour, int start = 0, int end = 10);
void setupController();
void connectMQTT();

// Make clients.
WiFiClient espClient;
HTTPClient http;
PubSubClient client(espClient);

// LED
#define NUM_LEDS 10
#define DATA_PIN 15
CRGB leds[NUM_LEDS];

bool alarmOn = false;

// MQTT.
char *mqtt_server;
char *mqtt_username;
char *mqtt_psw;
char *mqtt_topic;

#define ANN_BUFFER_SIZE (17)
#define ID_BUFFER_SIZE (4)
char announcement[ANN_BUFFER_SIZE];
char client_ID[ID_BUFFER_SIZE];
bool doorUnlocked = false;
int controller_ID = 1;

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Lcd.setTextColor(0xE4DFDA);
	FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS); // GRB ordering is assumed
	FastLED.setBrightness(40);

	// setupController();

	M5.Lcd.setTextSize(2);
	M5.Lcd.setCursor(0, 25);
	M5.Lcd.println("Status: ");
	pinMode(36, INPUT);
	// Task 1
    xTaskCreatePinnedToCore(motionSensor, "motionSensor", 4096, NULL, 2, NULL, 0);
}

void loop()
{
	// put your main code here, to run repeatedly:
	if (M5.BtnB.wasPressed())
	{
		unlockDoor();
		doorUnlocked = true;
	}

	if (M5.BtnC.wasPressed() && alarmOn)
	{
		alarmOn = false;
	}

	delay(1);
	M5.update();
}

void motionSensor(void* param)
{
	while (true)
	{

		M5.Lcd.fillRect(90, 25, 180, 50, BLACK);
		// Turn OFF led
		setLEDStrip(0x0);

		if (!doorUnlocked)
		{
			if (digitalRead(36) == 1)
			{ // If pin 36 reads a value of 1.
				M5.Lcd.setCursor(95, 25);
				M5.Lcd.print("Sensing");
				alarmOn = true;
				// LEDs
				if (alarmOn)
				{
					setLEDStrip(0xFF0000, 0, 5); // Set LED colour to RED
					setLEDStrip(0x0000FF, 5);	 // Set LED colour to BLUE
					delay(500);
					setLEDStrip(0x0000FF, 0, 5); // Set LED colour to BLUE
					setLEDStrip(0xFF0000, 5);	 // Set LED colour to RED
					delay(500);
				}
				// Turn OFF led
				setLEDStrip(0x0);
			}
			else
			{
				M5.Lcd.setCursor(95, 25);
				M5.Lcd.print("Not Sensed");
				alarmOn = false;
			}
		}
		else
		{
			M5.Lcd.fillRect(90, 25, 180, 50, BLACK);
			M5.Lcd.setCursor(95, 25);
			M5.Lcd.print("Not turned on");
			delay(5000);
			doorUnlocked = false;
		}
		delay(500);
	}
}

void connectToWifi(char *ssid, char *psw)
{
	WiFi.mode(WIFI_STA);
	WiFi.begin(ssid, psw);
	while (WiFi.status() != WL_CONNECTED)
	{
		delay(500);
		M5.Lcd.print(".");
	}
	M5.Lcd.println("Success");
}

char *getWifiSSID()
{
	// return "Room Of Requirements";
	return "Linksys07043";
}

String httpLogin()
{
	http.begin("http://192.168.1.100:8000/login");
	http.addHeader("Content-Type", "application/x-www-form-urlencoded");
	const char *headerKeys[] = {"Authorization"};
	http.collectHeaders(headerKeys, 1);
	int responseCode = http.POST("username=controller&password=contr0llerPassw0rd");
	String accessToken = http.header("Authorization");
	http.end();
	return accessToken;
}

char *getStorage()
{
	String accessToken = httpLogin();

	http.begin("http://192.168.1.100:8000/storage");
	http.addHeader("Authorization", accessToken);
	http.GET();
	http.end();
	return "Lager Syd";
}

void unlockDoor()
{
	String accessToken = httpLogin();
	M5.Lcd.setTextSize(1);
	Numpad numpad;

	char *doorCode = numpad.start();

	// http.begin("http://192.168.1.100:8000/unlockDoor");
	// http.addHeader("Authorization", accessToken);

	// http.addHeader("Content-Type", "application/json");
	// int responseCode = http.POST("username=controller&password=contr0llerPassw0rd");
	// http.end();

	M5.Lcd.setTextSize(2);
	M5.Lcd.setCursor(0, 25);
	M5.Lcd.println("Status: ");
}

// Function
void setLEDStrip(int colour, int start, int end)
{
	for (int i = start; i < end; i++)
	{
		leds[i] = colour;
	}
	FastLED.show();
}

void setupController()
{
	// Wifi.
	Keyboard keyboard;
	char *ssid = getWifiSSID();
	char *psw = keyboard.start();
	connectToWifi(ssid, psw);
	delay(1000);
	M5.Lcd.clear();
	char *storage = getStorage();
	char *controller = keyboard.start();
}

void connectMQTT()
{
	int value = 0;

	while (!client.connected())
	{
		M5.lcd.setTextSize(1); // Set font-size to 1
		M5.Lcd.println("Forsoeger MQTT forbindelse...");
		// Attempt to connect.
		if (client.connect(client_ID, "client", "pass"))
		{
			M5.Lcd.printf("Succes\n");
			// Once connected, publish an announcement to the topic.
			snprintf(announcement, ANN_BUFFER_SIZE, "Controller %d connected", controller_ID); // Format to the specified string and store it in a variable.

			client.publish(mqtt_topic, announcement);
			M5.lcd.setTextSize(2); // Change font-size back to 2
		}
		else
		{
			M5.Lcd.print("Fejl, rc=");
			M5.Lcd.println(client.state());
			M5.Lcd.println("Proever igen om 5 sekunder");

			value++;

			delay(10000);
			if (value % 7 == 0)
			{
				M5.Lcd.setCursor(0, 56);
				M5.lcd.fillRect(0, 56, 320, 184, BLACK); // Fill the screen with black.
			}
		}
	}
}
