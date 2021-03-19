# -*- coding: utf-8 -*-

import speech_recognition as sr       #importacion de librerias para el reconicimiento de voz
import _portaudio as r
 
r = sr.Recognizer() 

from opcua import Client         #importacion de librerias para la comunicacion por OPC-UA
from opcua import ua

url = "opc.tcp://192.168.1.150:4840"          # crear conexion cliente-servidor
client = Client(url)
client.connect()

from gtts import gTTS              #importacion de librerias para el reconicimiento de voz
from playsound import playsound
title = 1000

while True: 
    with sr.Microphone() as source:
        print('Te escucho : ')
        audio = r.listen(source)     # poner el micro en escucha

        try:
            text = r.recognize_google(audio, language="es-ES")  # pasa a atexto el audio escuchado
            print('Digiste: {}'.format(text))
            
            Usuario = client.get_node('ns=4; i=5')    # envia el texto a la variable designada en el PLC
            Us = ua.DataValue(ua.Variant(text, ua.VariantType.String))
            Usuario.set_data_value(Us)
    
            comparacion = ('dime el estado de las entradas'== text) 
      
            if comparacion == True:      # leer el estado de las variables 
                Entrada00 = client.get_node('ns=4; i=19')
                Entrada00 = Entrada00.get_value()
                texto1 = int(Entrada00) 

                Entrada01 = client.get_node('ns=4; i=20')
                Entrada01 = Entrada01.get_value()
                texto2 = int(Entrada01)

                Entrada02 = client.get_node('ns=4; i=21')
                Entrada02 = Entrada02.get_value()
                texto3 = int(Entrada02)

                Entrada03 = client.get_node('ns=4; i=22')
                Entrada03 = Entrada03.get_value()
                texto4 = int(Entrada03)
                
                Entrada04 = client.get_node('ns=4; i=23')
                Entrada04 = Entrada04.get_value()
                texto5 = int(Entrada04)
                
                Entrada05 = client.get_node('ns=4; i=24')
                Entrada05 = Entrada05.get_value()
                texto6 = int(Entrada05)


                entradas = "la entrada 1 es" + str(texto1) + "la entrada 2 es" + str(texto2)+ "la entrada 3 es" + str(texto3) + "la entrada 4 es" + str(texto4) + "la entrada 5 es" + str(texto5) + "la entrada 6 es" + str(texto6)


                lenguaje = 'es-ES'
                
                titulo = str(title) + '.mp3'
                print(titulo)
                
                audio = gTTS(text = entradas, lang = lenguaje, slow = True)
                audio.save(titulo) #guarda en un archivo .mp3 el texto como audio
                title = title + 1
                
                playsound(titulo)    #reproduce el archivo grabado
            else:
                print('Error')
        except:
            print('No te entiendo')
 
