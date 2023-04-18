// Official libaries.
#include <Arduino.h>
#include <M5Stack.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <HTTPClient.h>

// Own Files.
#include "keyboard.h"

void connectToWifi(char *ssid, char *psw);
char *getWifiSSID();
char *getStorage();
void setupController();
void connectMQTT();

WiFiClient espClient;
PubSubClient client(espClient);

// MQTT.
char *mqtt_server;
char *mqtt_username;
char *mqtt_psw;
char *mqtt_topic;

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (60)
#define ANN_BUFFER_SIZE (17)
#define ID_BUFFER_SIZE (4)
char announcement[ANN_BUFFER_SIZE];
char msg[MSG_BUFFER_SIZE];
char display_temp[MSG_BUFFER_SIZE];
char display_humi[MSG_BUFFER_SIZE];
char client_ID[ID_BUFFER_SIZE];
bool running;
int controller_ID = 1;

void setup()
{
	// put your setup code here, to run once:
	M5.begin();
	M5.Lcd.setTextColor(0xE4DFDA);
	M5.Lcd.setTextSize(2);
	M5.Lcd.println("PIR example");
	M5.Lcd.setCursor(0, 25);
	M5.Lcd.println("Status: \nValue: ");
	pinMode(36, INPUT);

	//setupController();
}

void loop()
{
	// put your main code here, to run repeatedly:
	M5.Lcd.fillRect(90, 25, 180, 50,
                    BLACK);  // Draw a black rectangle 180 by 50 at (90,25).
                             // 在(90,25)处画一个宽180高50的黑的矩形
    if (digitalRead(36) == 1) {  // If pin 36 reads a value of 1.  如果36号引脚的读取到的值为1
        M5.Lcd.setCursor(95, 25);
        M5.Lcd.print("Sensing");
        M5.Lcd.setCursor(95, 45);
        M5.Lcd.print("1");
    } else {
        M5.Lcd.setCursor(95, 25);
        M5.Lcd.print("Not Sensed");
        M5.Lcd.setCursor(95, 45);
        M5.Lcd.print("0");
    }
    delay(500);
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
            snprintf(announcement, ANN_BUFFER_SIZE, "Zone %d connected", controller_ID); // Format to the specified string and store it in a variable.

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
