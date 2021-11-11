import socket
import threading

class Server:
    def __init__(self):
        self.__HEADER = 8
        self.__PORT = 5000
        self.__SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
        self.__ADDRESS = (self.__SERVER, self.__PORT) #Makes a tuple for the address
        self.__FORMAT = 'utf-8'

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
        self.__server.bind(self.__ADDRESS)

    def GetMsgs(self, conn, addr):
        #receiving messages
        msgLen = conn.recv(self.__HEADER).decode(self.__FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
        if msgLen:  #First message will always be empty
            msgLen = int(msgLen)
            msg = conn.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
            
            if msg.upper() == "!DISCONNECT":
                conn.close()
            
            if msg != "":
                print(str(addr) +  ":", str(msg)) #Prints the message

    def SendMsg(self, newMsg, conn):
        encMessage = newMsg.encode(self.__FORMAT) #encodes msg with utf-8
        msgLen = len(encMessage)
        msgLen = str(msgLen).encode(self.__FORMAT) 
        msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
        #b' ' means the byte representation of a space
        conn.send(msgLen)
        conn.send(encMessage)
        newMsg = ""
        return newMsg

    def HandleClient(self, conn, addr):
        print(f"New Client: {addr}")  #Outputs the new client's local address
        newMsg = "Connection established"
        #create new thread for getting messages
        while True: 
            self.GetMsgs(conn, addr)
            #sending messages
            if newMsg:
                newMsg = self.SendMsg(newMsg, conn)
            #put stuff here for server to do to change newMsg

    def GetClient(self):
        self.__server.listen() #Looks for connections
        while True:
            conn, addr = self.__server.accept() #When connection occurs
            thread = threading.Thread(target=self.HandleClient, args=(conn, addr)) #Makes a new thread for the client handling so when it listens it doesn't stop the whole program
            thread.start()  #Starts the thread

#server starts here
server = Server()
print("Starting server")
server.GetClient()