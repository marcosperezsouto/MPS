#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient

topics = ['Temperatura', 'Presion', 'Amperios', 'Litros']

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    try:
        for topic in topics:
            client.subscribe(topic)
        print("subscribed")
    except:
        print("exception")

    
def on_message(client, userdata, msg):
    print("Received a message on topic: " + msg.topic)
    # Use utc as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=msg.payload.decode("utf-8")
    isfloatValue=False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue=True
    except:
        print("Could not convert " + message + " to a float value")
        isfloatValue=False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))

        json_body = [
            {
                "measurement": msg.topic,
                "time": receiveTime,
                "fields": {
                    "value": val
                }
            }
        ]

        dbclient.write_points(json_body)
        print("Finished writing to InfluxDB")
        
# Set up a client for InfluxDB
dbclient = InfluxDBClient('192.168.8.105', 8086, 'mqtt', 'mqtt', 'mqtt_pruebas')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("192.168.8.105", 1883, 60)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
