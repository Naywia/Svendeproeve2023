import paho.mqtt.client as mqtt #import the client
import json


class Mosquitto:

    def __init__(self):
        self.client = mqtt.Client() #create new instance
        self.client.username_pw_set("user", "P@ssw0rd!")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("127.0.0.1", 1883) #connect to broker

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if the connection is lost and reconnected, then subscriptions will be renewed.
        client.subscribe("security")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")

        if "{" in payload:
            data = json.loads(payload)

            print(payload + " received on topic[" + msg.topic + "]")

            payload="zone_id=" + str(data["zone_ID"]) + "&log_action_id=7" + "&temperature=" + data["temperature"] + "&humidity=" + data["humidity"] + "&alarm=0"

            print(response.text)

        else:
            print(payload)





#client.loop_forever()
