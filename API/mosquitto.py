import paho.mqtt.client as mqtt #import the client
from json import loads
from requests import request as req

url="http://127.0.0.1:8000"
host="127.0.0.1"
username="client"
password="pass"

# Headers
headers = {
    'Authorization': 'Bearer 14c41540aa68c8108e51a7ed017681bdb9dc8e89eeffcd20e673597b84249bc0df01af90ccc91774e559c70ee0c3b6856f0eb930657ddfd62a7631a0f374f608',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if the connection is lost and reconnected, then subscriptions will be renewed.
    client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")

    if "{" in payload:
        data = loads(payload)

        print(payload + " received on topic[" + msg.topic + "]")

        payload="zone_id=" + str(data["zone_ID"]) + "&log_action_id=7" + "&temperature=" + data["temperature"] + "&humidity=" + data["humidity"] + "&alarm=0"

        response=req("POST", url, headers=headers, data=payload)

        print(response.text)

    else:
        print(payload)

client = mqtt.Client() #create new instance
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)

client.connect(host, 1883) #connect to broker

client.loop_forever()
