#!/usr/bin/env python3

import json
import os
import csv
from opcua import Client
import datetime
import time

url = "opc.tcp://192.168.8.150:4840"
client = Client(url)

date_json = os.path.join(os.path.dirname(__file__), 'date.json')
prueba1_csv = os.path.join(os.path.dirname(__file__), 'prueba1.csv')


try:
    with open(date_json, 'r') as date_file:
        date_data = json.load(date_file)
        print(date_data)
except:
    # crea diccionario
    date_data = {}

create_data = {}

def crear_csv(fichero, datos):
    with open(fichero, 'w') as f:
        csv_create = csv.writer(f)
        csv_create.writerow(['máquina', 'fecha', 'hora', 'temperatura', 'litros', 'amperios', 'presion'])
        
crear_csv(prueba1_csv, create_data)



client.connect()
print ("Client connected")

while True:

    def csv_prueba1(fichero, datos):
        with open(fichero, 'a') as f:
            csv_file = csv.writer(f)
            csv_file.writerow(['Prueba1', datos['fecha'], datos['hora'], datos['temperatura'], datos['litros'], datos['amperios'], datos['presion']])  


    fecha_str = datetime.date.today().isoformat()
    date_data['fecha'] = fecha_str

    hora_str = time.strftime("%H:%M")
    date_data['hora'] = hora_str

    Temp = client.get_node('ns=3; s="DATOS"."Temperatura"')
    Temperatura = Temp.get_value()
    date_data['temperatura'] = Temperatura

    Press = client.get_node('ns=3; s="DATOS"."Presion"')
    Presion = Press.get_value()
    date_data['presion'] = Presion

    Litros = client.get_node('ns=3; s="DATOS"."Litros"')
    Litros = Litros.get_value()
    date_data['litros'] = Litros

    Amp = client.get_node('ns=3; s="DATOS"."Amperios"')
    Amperios = Amp.get_value()
    date_data['amperios'] = Amperios


    print(date_data)

    csv_prueba1(prueba1_csv, date_data)

    time.sleep(5)





