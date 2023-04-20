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
void buttons();
void motionSensor();
void check();
void alarm();
void connectToWifi(char *ssid, char *psw);
char *getWifiSSID();
String httpLogin();
char *getStorage();
void unlockDoor();
void setLEDStrip(int colour, int start = 0, int end = 10);
void setupController();
void sendMQTT(char *topic, char *message);
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
#define MSG_BUFFER_SIZE (60)
char msg[MSG_BUFFER_SIZE];
char announcement[ANN_BUFFER_SIZE];
char client_ID[ID_BUFFER_SIZE];
char *storage;
char *controller;
int controller_ID = 1;

bool doorUnlocked = false;
#define REQ_BUFFER_SIZE (16)
char *sensing;

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Lcd.setTextColor(0xE4DFDA);
	FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS); // GRB ordering is assumed
	FastLED.setBrightness(40);

	setupController();
	client.setServer(mqtt_server, 1883);
	// Connect to MQTT client
    connectMQTT();

	// M5.Lcd.setTextSize(2);
	// M5.Lcd.setCursor(0, 25);
	// M5.Lcd.println("Status: ");
	buttons();
	pinMode(36, INPUT);
}

void loop()
{
	// put your main code here, to run repeatedly:
	check();

	if (!doorUnlocked)
	{
		motionSensor();
		delay(500);
	}
	else
	{
		// M5.Lcd.fillRect(90, 25, 180, 50, BLACK);
		// M5.Lcd.setCursor(95, 25);
		// M5.Lcd.print("Not turned on");
		sensing = "Not turned on";
		M5.update();
		delay(5000);
		doorUnlocked = false;
	}

	delay(1);
	M5.update();
}

void buttons()
{
	// Setup
	M5.Lcd.drawRect(0, 208, 106, 32, BLUE);
	M5.Lcd.drawRect(106, 208, 107, 32, BLUE);
	M5.Lcd.drawRect(213, 208, 106, 32, BLUE);
	M5.Lcd.drawString("Se Status", 30, 215, 2);		// Default first num 80
	M5.Lcd.drawString("Laas doer op", 123, 215, 2); // Default first num 80
	M5.Lcd.drawString("Sluk alarm", 230, 215, 2);	// Default first num 80
}

void motionSensor()
{
	// M5.Lcd.fillRect(90, 25, 180, 50, BLACK);
	// Turn OFF led
	setLEDStrip(0x0);
	if (digitalRead(36) == 1)
	{ // If pin 36 reads a value of 1.
		// M5.Lcd.setCursor(95, 25);
		// M5.Lcd.print("Sensing");
		sensing = "Sensing";
		alarmOn = true;
		snprintf(msg, MSG_BUFFER_SIZE, "{\"controller_ID\": %d, \"incident\": \"Movement detected in %s\", \"incidentDate\": %s, \"logTypeID\": %d}", controller_ID, storage, "25-04-2023", 1);
		client.publish("security", msg);
	}
	else
	{
		// M5.Lcd.setCursor(95, 25);
		// M5.Lcd.print("Not Sensed");
		sensing = "Not Sensed";
		alarmOn = false;
	}

	alarm();
}

void check()
{
	if (M5.BtnA.wasPressed())
	{
		M5.Lcd.fillRect(90, 25, 180, 50, BLACK);
		M5.Lcd.setCursor(0, 25);
		M5.Lcd.println("Status: ");
		M5.Lcd.setCursor(95, 25);
		M5.Lcd.print(sensing);
	}

	if (M5.BtnB.wasPressed())
	{
		M5.Lcd.clear();
		unlockDoor();
	}

	if (M5.BtnC.wasPressed() && alarmOn)
	{
		alarmOn = false;
	}
}

void alarm()
{
	// LEDs
	if (alarmOn)
	{
		check();
		setLEDStrip(0xFF0000, 0, 5); // Set LED colour to RED
		setLEDStrip(0x0000FF, 5);	 // Set LED colour to BLUE
		M5.update();
		delay(500);
		check();
		setLEDStrip(0x0000FF, 0, 5); // Set LED colour to BLUE
		setLEDStrip(0xFF0000, 5);	 // Set LED colour to RED
		M5.update();
		delay(500);
	}
	// Turn OFF led
	setLEDStrip(0x0);
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
	M5.Lcd.setTextSize(1);
	Numpad numpad;

	char *doorCode = numpad.start();
	String accessToken = httpLogin();

	http.begin("http://192.168.1.100:8000/unlockDoor");
	http.addHeader("Authorization", accessToken);

	http.addHeader("Content-Type", "application/json");
	char *string = "\"doorCode\":";
	char request[REQ_BUFFER_SIZE];
	int i;
	for (i = 0; i < strlen(string); i++)
	{
		request[i] = string[i];
	}
	for (int j = 0; j < strlen(doorCode); j++)
	{
		request[i] = doorCode[j];
		i++;
	}

	int responseCode = http.POST(request);
	http.end();

	if (responseCode == 200)
	{
		doorUnlocked = true;
		setLEDStrip(0x00FF00);
		delay(500);
		setLEDStrip(0x0);
	}
	else
	{
		setLEDStrip(0xFF0000);
		delay(500);
		setLEDStrip(0x0);
	}

	buttons();
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
	// char *psw = keyboard.start();
	char *psw = "5h0cpt1iug";
	connectToWifi(ssid, psw);
	delay(1000);
	M5.Lcd.clear();
	// storage = getStorage();
	// controller = keyboard.start();
}

void connectMQTT()
{
	int value = 0;

	while (!client.connected())
	{
		M5.lcd.setTextSize(1); // Set font-size to 1
		M5.Lcd.println("Forsoeger MQTT forbindelse...");
		// Attempt to connect.
		if (client.connect(client_ID, "user", "P@ssw0rd!"))
		{
			M5.Lcd.printf("Succes\n");
			// Once connected, publish an announcement to the topic.
			// snprintf(announcement, ANN_BUFFER_SIZE, "{\"controller\": %s, \"storage\": \"%i\"}", controller, storage); // Format to the specified string and store it in a variable.

			// client.publish("new_controller", announcement);
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
