import socket

HEADER = 8
PORT = 5000
SERVER = "192.168.1.125"
FORMAT = 'utf-8'
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Same as before, ipv4 and TCP
client.connect(ADDRESS) #Connects to the right local address, in this case its my own pc

def SendMsg(msg):
    encMessage = msg.encode(FORMAT) #encodes msg with utf-8
    msgLen = len(encMessage)
    msgLen = str(msgLen).encode(FORMAT) 
    msgLen += b' ' * (HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
    #b' ' means the byte representation of a space
    client.send(msgLen)
    client.send(encMessage)

SendMsg("TestMsg 1")