# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

    client.subscribe('CMD/10000/data', 2)
    client.subscribe('CMD/10000/upload_log', 2)

# The callback for when a PUBLISH message is received from the server.
def on_subscribe(client, userdata, msg, rc):
    print 'subscribe'
    print msg, rc


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_publish(client, userdata, mid):
    print 'publish'


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish

client.username_pw_set('cmdata', '@ICHAOmeng2016')
client.connect("123.57.238.5", 1883, 20)

client.loop_forever()
