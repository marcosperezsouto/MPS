# -*- coding: latin-1 -*-

import cv2                 #importacion de librerias para el reconicimiento de imagenes
import face_recognition    #importacion de librerias para el reconicimiento facial

from opcua import Client    #importacion de librerias para la comunicacion por OPC_UA
from opcua import ua

url = "opc.tcp://192.168.1.150:4840"      # crear conexion cliente-servidor
client = Client(url)
client.connect()
  
#Cargar la imagen de ejemplo con nuestro rostro (tiene que estar en el mismo directorio que este archivo)
imagen_personal = face_recognition.load_image_file("marcos.jpg")
 
#Extraer los 'encodings' que caracterizan nuestro rostro:
personal_encodings = face_recognition.face_encodings(imagen_personal)[0]
 
#Definir un array con los encodings y nuestro nombre:
encodings_conocidos = [
    personal_encodings
]
nombres_conocidos = [
    "marcos"
]
 
#Iniciar la webcam:
webcam = cv2.VideoCapture(0)

#Cargar una fuente de texto:
font = cv2.FONT_HERSHEY_COMPLEX
 
#Sin que haya retardo vamos a reducir el tamaño de la imagen de la webcam.
reduccion = 5 #Con un 5, la imagen se reducir a 1/5 del tamaño original
 
while 1:
    loc_rostros = []        #Localizacion de los rostros en la imagen
    encodings_rostros = []  #Encodings de los rostros
    nombres_rostros = []    #Nombre de la persona de cada rostro
    nombre = ""             #Variable para almacenar el nombre
 
    valido, img = webcam.read()   #Capturamos una imagen con la webcam

#Si la imagen es valida (es decir, si se ha capturado correctamente), continuamos:
    if valido:
 
        #La imagen esta en el espacio de color BGR, habitual de OpenCV. Hay que convertirla a RGB:
        img_rgb = img[:, :, ::-1]
 
        #Reducimos el tamaño de la imagen para que sea mas rapida de procesar:
        img_rgb = cv2.resize(img_rgb, (0, 0), fx=1.0/reduccion, fy=1.0/reduccion)
 
        #Localizamos cada rostro de la imagen y extraemos sus encodings:
        loc_rostros = face_recognition.face_locations(img_rgb)
        if loc_rostros == []:
            Usuario = client.get_node('ns=4; i=3')      # envia el texto a la variable designada en el PLC
            Us = ua.DataValue(ua.Variant('¿¿¿', ua.VariantType.String))
            Usuario.set_data_value(Us)
        else:
            print('ok')
        encodings_rostros = face_recognition.face_encodings(img_rgb, loc_rostros)


        #Recorremos el array de encodings que hemos encontrado:
        for encoding in encodings_rostros:
 
            #Buscamos si hay alguna coincidencia con algun encoding conocido:
            coincidencias = face_recognition.compare_faces(encodings_conocidos, encoding)

            #El array 'coincidencias' es ahora un array de booleanos. Si contiene algun 'True', es que ha habido alguna coincidencia:
            if True in coincidencias:
                nombre = nombres_conocidos[coincidencias.index(True)]
                
                Usuario = client.get_node('ns=4; i=3')     # envia el texto a la variable designada en el PLC
                Us = ua.DataValue(ua.Variant(nombre, ua.VariantType.String))
                Usuario.set_data_value(Us)

            #Si no hay ningun 'True' en el array 'coincidencias', no se ha podido identificar el rostro:
            else:
                nombre = "???"
                
                Usuario = client.get_node('ns=4; i=3')
                Us = ua.DataValue(ua.Variant('¿¿¿', ua.VariantType.String))
                Usuario.set_data_value(Us) 
                
            #Añadir el nombre de la persona identificada en el array de nombres:
            nombres_rostros.append(nombre)

        #Dibujamos un recuadro rojo alrededor de los rostros desconocidos, y uno verde alrededor de los conocidos:
        for (top, right, bottom, left), nombre in zip(loc_rostros, nombres_rostros):
             
            #Deshacemos la reduccion de tamaño para tener las coordenadas de la imagen original:
            top = top*reduccion
            right = right*reduccion
            bottom = bottom*reduccion
            left = left*reduccion

            #Cambiar de color segun si se ha identificado el rostro:
            if nombre != "???":
                color = (0,255,0)
            else:
                color = (0,0,255)
                
                Usuario = client.get_node('ns=4; i=3')
                Us = ua.DataValue(ua.Variant('¿¿¿', ua.VariantType.String))
                Usuario.set_data_value(Us) 
                
            #Dibujar un rectangulo alrededor de cada rostro identificado, y escribir el nombre:
            cv2.rectangle(img, (left, top), (right, bottom), color, 2)
            cv2.rectangle(img, (left, bottom - 20), (right, bottom), color, -1)
            cv2.putText(img, nombre, (left, bottom - 6), font, 0.6, (0,0,0), 1)
         
        #Mostrar el resultado en una ventana:
        cv2.imshow('Output', img)

        #Salir con 'ESC'
        k = cv2.waitKey(5) & 0xFF
        
        if k == 27:
            cv2.destroyAllWindows()
            break     

webcam.release()