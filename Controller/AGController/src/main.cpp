// Official libaries.
#include <Arduino.h>
#include <M5Stack.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>
#include <FastLED.h>
#include <time.h>

// Own Files.
// #include "keyboard.h"
#include "wificonnector.h"
#include "numpad.h"

// Initate functions.
String httpLogin();
void setupController();
char *getWifiSSID();
char *getStorage();
void connectMQTT();

void checkButtonClick();
char *getDateTime();
void motionSensor();
void alarm();
void unlockDoor();

void drawButtons();

// Make clients.
WiFiClient espClient;
HTTPClient http;
PubSubClient client(espClient);

WiFiConnector wifiConnector;

// LED
Leds led;

// Checks
bool alarmOn = false;
bool doorUnlocked = false;
bool sent = false;

// MQTT.
char *mqtt_server = "192.168.1.100";
#define ANN_BUFFER_SIZE (17)
#define ID_BUFFER_SIZE (4)
#define MSG_BUFFER_SIZE (200)
char msg[MSG_BUFFER_SIZE];
char announcement[ANN_BUFFER_SIZE];
char client_ID[ID_BUFFER_SIZE];
char *storage;
char *controller;
int controller_ID = 1;

// Motion sensor
char *sensing;

// Requests
#define REQ_BUFFER_SIZE (16)

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Power.begin();
	M5.Lcd.setTextColor(0xE4DFDA);

	setupController();

	// LEDs
    led.initLED();
	led.setLEDStrip(0x0);
		
	// Connect to MQTT client
	client.setServer(mqtt_server, 1883);
	connectMQTT();

	drawButtons();
	pinMode(36, INPUT);
}

void loop()
{
	// put your main code here, to run repeatedly:
	client.loop();
	checkButtonClick();

	if (!doorUnlocked)
	{
		motionSensor();
		delay(500);
	}
	else
	{
		sensing = "Not turned on";
		M5.update();
		delay(5000);
		doorUnlocked = false;
	}

	delay(1);
	M5.update();
}

// HTTP
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

// Setup functions
void setupController()
{
	// Wifi.
	
	Keyboard keyboard;
	char *ssid = getWifiSSID();
	wifiConnector.connectToWiFi(ssid);
	// char *psw = "5h0cpt1iug";
	delay(1000);
	M5.Lcd.clear();
	// storage = getStorage();
	// controller = keyboard.start();
}

char *getWifiSSID()
{
	// return "Room Of Requirements";
	return "Linksys07043";
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

			delay(1000);
			M5.Lcd.clear();
			// Once connected, publish an announcement to the topic.
			// snprintf(announcement, ANN_BUFFER_SIZE, "{\"controller\": %s, \"storage\": \"%i\"}", controller, storage); // Format to the specified string and store it in a variable.

			// client.publish("new_controller", announcement);
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

// Logic functions.
void checkButtonClick()
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
		sent = false;
	}
}

char *getDateTime()
{
	const int daylightSavingTime = 3600;
	const long gmtOffset_sec = 1;
	const int daylightOffset_sec = 3600 + daylightSavingTime;
	configTime(gmtOffset_sec, daylightOffset_sec, "dk.pool.ntp.org");
	M5.Lcd.setCursor(0, 47); // Set cursor to (0,47).
	// Output current time.
	struct tm timeinfo;
	char buffer[80];

	if (!getLocalTime(&timeinfo))
	{
		// Return 1 when the time is successfully obtained.
		M5.Lcd.println("Failed to obtain time");
		
	}
	strftime(buffer, 80, "%d-%m-%Y %H:%M:%S", &timeinfo); // Screen prints date and time.
	return buffer;
}

void motionSensor()
{
	// Turn OFF led
	led.setLEDStrip(0x0);
	if (digitalRead(36) == 1)
	{
		sensing = "Sensing";
		alarmOn = true;
		if (!sent)
		{
			char *dt = getDateTime();
			snprintf(msg, MSG_BUFFER_SIZE, "{\"controllerID\": %d, \"incident\": \"Movement detected in Lager Syd\", \"incidentDate\": \"26-04-2023 9:21:35\", \"logTypeID\": %d}", controller_ID, 1);
			// M5.Lcd.drawString(msg, 0, 100, 2);
			client.publish("security", msg);
			sent = true;
		}
	}
	else
	{
		sensing = "Not Sensed";
		alarmOn = false;
	}

	alarm();
}

void alarm()
{
	// LEDs
	if (alarmOn)
	{
		checkButtonClick();
		M5.update();
		led.setLEDStrip(0xFF0000, 0, 5); // Set LED colour to RED
		led.setLEDStrip(0x0000FF, 5);	 // Set LED colour to BLUE
		delay(500);
		checkButtonClick();
		M5.update();
		led.setLEDStrip(0x0000FF, 0, 5); // Set LED colour to BLUE
		led.setLEDStrip(0xFF0000, 5);	 // Set LED colour to RED
		delay(500);
	}
	// Turn OFF led
	led.setLEDStrip(0x0);
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
		led.setLEDStrip(0x00FF00);
		delay(500);
		led.setLEDStrip(0x0);
	}
	else
	{
		led.setLEDStrip(0xFF0000);
		delay(500);
		led.setLEDStrip(0x0);
	}

	drawButtons();
}

// Style Functions
void drawButtons()
{
	// Setup
	M5.Lcd.drawRect(0, 208, 106, 32, BLUE);
	M5.Lcd.drawRect(106, 208, 107, 32, BLUE);
	M5.Lcd.drawRect(213, 208, 106, 32, BLUE);
	M5.Lcd.drawString("Se Status", 30, 215, 2);		// Default first num 80
	M5.Lcd.drawString("Laas doer op", 123, 215, 2); // Default first num 80
	M5.Lcd.drawString("Sluk alarm", 230, 215, 2);	// Default first num 80
}
