
import paho.mqtt.client as mqtt
import time

print('Iniciando programa')
           
broker_address="192.168.1.137"
client = mqtt.Client('MQTTInfluxDBprueba')
client.connect(broker_address)

topic = "Amperios"
payload = "25"
client.publish(topic, payload)
