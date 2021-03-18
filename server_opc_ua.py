
import time
import datetime
from opcua import ua, Server



# setup our server
server = Server()
url = "opc.tcp://192.168.8.108:4840"
server.set_endpoint(url)

name = "opc-ua server"
addspace = server.register_namespace(name)

node = server.get_objects_node()

# populating our address space
Param  = node.add_object(addspace, "Parametros")
Temp = Param.add_variable(addspace, "Temteratura", 0)
Press = Param.add_variable(addspace, "Presion", 0)
L = Param.add_variable(addspace, "Litros", 0)
Amp = Param.add_variable(addspace, "Amperios", 0)


Temp.set_writable()    # Set MyVariable to be writable by clients
Press.set_writable()
L.set_writable()
Amp.set_writable()


# starting!
server.start()
print ("Server started at {}".format(url))
    
try:
    Temperatura = 10
    Presion = 6.0
    Litros = 1
    Amperios = 10

    while True:

        print (Temperatura, Presion, Litros, Amperios)

       
        Temp.set_value(Temperatura)
        Press.set_value(Presion) 
        Amp.set_value(Amperios)       
        L.set_value(Litros)        

        Temperatura = Temperatura + 1
        Presion = Presion + 0.1
        Amperios = Amperios + 1
        Litros = Litros + 5
        
        time.sleep(2)

finally:
    #close connection, remove subcsriptions, etc
    server.stop()
