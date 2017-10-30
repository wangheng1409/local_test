# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # out_dict = {'barcodes': {'6954767410173': 'http://b.ichaomeng.com:12344/ads?b=6954767410173', \
    #                          '6921317905380': 'http://b.ichaomeng.com:12344/ads?b=6921317905380', \
    #                          '12345': 'haha'},
    #             'version': 'v1'}

    # print client.publish(topic='CMD/10000/config', payload=json.dumps(out_dict))


    print client.publish(topic='CMD/10000/upload_log', payload='upload')


# # The callback for when a PUBLISH message is received from the server.
# def on_subscribe(client, userdata, msg, rc):
#     print 'subscribe'
#     print msg, rc


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload)),'message'

def on_publish(client, userdata, mid):
    print 'publish'
    print userdata
    print mid


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.on_subscribe = on_subscribe
client.on_publish = on_publish

client.username_pw_set('cmdata', '@ICHAOmeng2016')
client.connect('123.57.238.5', 1883, 20)

client.loop_forever()
