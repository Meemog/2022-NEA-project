import socket
import threading

class Client:
    def __init__(self):
        self.__HEADER = 8
        self.__PORT = 5000
        self.__SERVER = socket.gethostbyname(socket.gethostname()) #temporary // sets ip of host to client ip, which is same as host ip
        self.__FORMAT = 'utf-8'
        self.__ADDRESS = (self.__SERVER, self.__PORT)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Same as before, ipv4 and TCP
        self.__client.connect(self.__ADDRESS) #Connects to the right local address, in this case its my own pc

    def SendMsg(self, msg):
        encMessage = msg.encode(self.__FORMAT) #encodes msg with utf-8
        msgLen = len(encMessage)
        msgLen = str(msgLen).encode(self.__FORMAT) 
        msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
        #b' ' means the byte representation of a space
        self.__client.send(msgLen)
        self.__client.send(encMessage)

    def GetMsgs(self):
        while True:
            msgLen = self.__client.recv(self.__HEADER).decode(self.__FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
            if msgLen:  #First message will always be empty
                msgLen = int(msgLen)
                msg = self.__client.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
                if msg != "":
                    print(f"\nMessage from server: {str(msg)}")

client = Client()
receiveThread = threading.Thread(target=client.GetMsgs)
receiveThread.start()

newMsg = "hello"
while True:
    client.SendMsg(newMsg)
    newMsg = input("Client message to server:")
