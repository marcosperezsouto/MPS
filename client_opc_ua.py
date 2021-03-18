

from opcua import Client
import time


url = "opc.tcp://192.168.8.109:4840"
client = Client(url)
# client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user

client.connect()
print ("Client connected")

while True:
    # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
    Temp = client.get_node("ns=2; i=2")
    Temperatura = Temp.get_value()
    print(Temperatura)

    Press = client.get_node("ns=2; i=3")
    Presion = Press.get_value()
    print(Presion)

    TIME = client.get_node("ns=2; i=4")
    Time_value = TIME.get_value()
    print(Time_value)

    # get a specific node knowing its node id
    #var = client.get_node(ua.NodeId(1002, 2))
    #var = client.get_node("ns=3;i=2002")
    #print(var)
    #var.get_data_value() # get value of node as a DataValue object
    #var.get_value() # get value of node as a python builtin
    #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
    #var.set_value(3.9) # set node value using implicit data type

    time.sleep(1)

    # Stacked myvar access
    # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())


