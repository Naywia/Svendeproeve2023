// Official libaries.
#include <Arduino.h>
#include <M5Stack.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>



// Own Files.
#include "keyboard.h"

void connectToWifi();
char *getWifiSSID();
char *getStorage();
void setupController();

// MQTT.
char *mqtt_server;
char *mqtt_username;
char *mqtt_psw;
char *mqtt_topic;

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Lcd.setTextColor(0xE4DFDA);
	M5.Lcd.setTextSize(1);

	setupController();
}

void loop()
{
	// put your main code here, to run repeatedly:
	
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
	return "Room Of Requirements";
}

char *getStorage()
{
	HTTPClient http;
	http.begin("http://192.168.1.100:8000/login");
	http.addHeader("Content-Type", "application/x-www-form-urlencoded");
	const char *headerKeys[] = {"Authorization"};
	http.collectHeaders(headerKeys, 1);
	int responseCode = http.POST("username=controller&password=contr0llerPassw0rd");
	String accessToken = http.header("Authorization");
	http.end();

	http.begin("http://192.168.1.100:8000/storage");
	http.addHeader("Authorization", accessToken);
	http.GET();
	http.end();
	return "Lager Syd";
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