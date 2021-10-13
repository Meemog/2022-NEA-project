import socket
import threading

HEADER = 8
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname()) #temporary // sets ip of host to client ip, which is same as host ip
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

def GetMsgs():
    while True:
        msgLen = client.recv(HEADER).decode(FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
        if msgLen:  #First message will always be empty
            msgLen = int(msgLen)
            msg = client.recv(msgLen).decode(FORMAT) #Waits for a message with length msgLen to be received
            if msg != "":
                print(f"\nMessage from server: {str(msg)}")

receiveThread = threading.Thread(target=GetMsgs)
receiveThread.start()

newMsg = "hello"
while True:
    SendMsg(newMsg)
    newMsg = input("Client message to server:")
