import socket
import threading

class ClientSocket:
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
        #Sets blocking to false
        self.__client.setblocking(False)
        #If a socket doesn't receive anything before timeout it returns a socket error
        try:
            msgLen = self.__client.recv(self.__HEADER).decode(self.__FORMAT)
        except socket.error:
            msgLen = 0
        self.__client.setblocking(True)

        msgLen = int(msgLen)    
        if msgLen > 0:  #First message will always be empty
            msg = self.__client.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
            if msg != "":
                return msg
        return ""

    def EndConnection(self):
        self.SendMsg("!DISCONNECT")
        self.__client.close()
        


# client = ClientSocket()
# receiveThread = threading.Thread(target=client.GetMsgs)
# receiveThread.start()

# newMsg = "hello"
# client.SendMsg(newMsg)
# while True:
#     newMsg = input("Client message to server:")
#     client.SendMsg(newMsg)
#     if newMsg == "!DISCONNECT":
#         break