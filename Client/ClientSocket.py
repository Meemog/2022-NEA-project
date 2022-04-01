import socket

class ClientSocket:
    def __init__(self):
        self.__HEADER = 8
        self.__PORT = 5000  
        self.__SERVER = socket.gethostbyname(socket.gethostname()) #temporary // sets ip of host to client ip, which is same as host ip
        self.__FORMAT = 'utf-8'
        self.__ADDRESS = (self.__SERVER, self.__PORT)
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Same as before, ipv4 and TCP
        self.__client.connect(self.__ADDRESS) #Connects to the right local address, in this case its my own pc
        self.connected = True

        self.msgsToSend = []
        self.receivedMsgs = []

    #Made to be used in a seperate thread
    #Checks if any messages need to be sent
    #Sends them to the server and removes them from the list
    def SendMsgs(self):
        self.__client.setblocking(False)
        unsentMessages = []
        while self.msgsToSend != []:
            message = self.msgsToSend.pop(0)
            try:
                encMessage = message.encode(self.__FORMAT) #encodes msg with utf-8
                msgLen = str(len(encMessage)).encode(self.__FORMAT) 
                msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
                #b' ' means the byte representation of a space
                self.__client.send(msgLen)
                self.__client.send(encMessage)
                print(f"Message Sent:{message}")
            except socket.error:
                unsentMessages.append(message)
        self.__client.setblocking(True)
        for message in unsentMessages:
            self.msgsToSend.append(message)

    def GetMsgs(self):
        self.__client.setblocking(False)
        msgLen = 0
        try:
            msgLen = self.__client.recv(self.__HEADER).decode(self.__FORMAT)
            msgLen = int(msgLen)
            if msgLen > 0:
                self.__client.setblocking(True)
                msg = self.__client.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
                self.receivedMsgs.append(msg)
                print(f"Message Received:{msg}")
        except socket.error:
            self.__client.setblocking(True)

    #This function needs to make sure the message is sent before closing the socket
    def EndConnection(self):
        encMessage = "!DISCONNECT".encode(self.__FORMAT) #encodes msg with utf-8
        msgLen = str(len(encMessage)).encode(self.__FORMAT) 
        msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
        #b' ' means the byte representation of a space
        self.__client.send(msgLen)
        self.__client.send(encMessage)
        
        self.connected = False