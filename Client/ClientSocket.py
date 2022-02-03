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
        self.connected = True

        self.msgsToSend = []
        self.__msgSendThread = threading.Thread(target=self.__SendMsgs, daemon=True)
        self.__msgSendThread.start()
        
        self.receivedMsgs = []
        self.__msgGetThread = threading.Thread(target=self.__GetMsgs, daemon=True)
        self.__msgGetThread.start()

    #Made to be used in a seperate thread
    #Checks if any messages need to be sent
    #Sends them to the server and removes them from the list
    def __SendMsgs(self):
        try:
            while self.connected:
                if self.msgsToSend != []:
                    msg = self.msgsToSend.pop(0)
                    encMessage = msg.encode(self.__FORMAT) #encodes msg with utf-8
                    msgLen = str(len(encMessage)).encode(self.__FORMAT) 
                    msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
                    #b' ' means the byte representation of a space
                    self.__client.send(msgLen)
                    self.__client.send(encMessage)
            return 0
        except:
            print("Connection closed by server2")
            self.connected = False

    def __GetMsgs(self):
        try:
            while self.connected:
                self.__client.setblocking(False)
                try:
                    msgLen = int(self.__client.recv(self.__HEADER).decode(self.__FORMAT))
                except socket.error:
                    msgLen = 0
                self.__client.setblocking(False)
                msgLen = int(msgLen)
                if msgLen > 0:  #First message will always be empty
                    msg = self.__client.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
                    if msg != "":
                        self.receivedMsgs.append(msg)
            return 0
        except:
            print("Connection closed by server1")
            self.connected = False

    #This function needs to make sure the message is sent before closing the socket
    def EndConnection(self):
        encMessage = "!DISCONNECT".encode(self.__FORMAT) #encodes msg with utf-8
        msgLen = len(encMessage)
        msgLen = str(msgLen).encode(self.__FORMAT) 
        msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
        #b' ' means the byte representation of a space

        self.connected = False
        self.__msgGetThread.join()
        self.__msgSendThread.join()

        #Sends disconnect message to server
        self.__client.send(msgLen)
        self.__client.send(encMessage)
        self.__client.close()