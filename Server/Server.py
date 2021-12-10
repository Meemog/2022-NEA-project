import socket
import threading
from Game import Game
from Player import Player

class Server:
    def __init__(self):
        self.__HEADER = 8
        self.__PORT = 5000
        self.__SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
        self.__ADDRESS = (self.__SERVER, self.__PORT) #Makes a tuple for the address
        self.__FORMAT = 'utf-8'

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
        self.__server.bind(self.__ADDRESS)

        print("[SERVER STARTED]")
        self.__server.setblocking(False)

    def GetMsgs(self, conn, addr):
        #receiving messages
        conn.setblocking(False)
        try:
            msgLen = conn.recv(self.__HEADER).decode(self.__FORMAT) #Waits for message with length 8 bytes to be received from the client and then decodes it 
        except socket.error:
            return " "

        if msgLen:  #First message will always be empty
            msgLen = int(msgLen)
            conn.setblocking(True)
            msg = conn.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
            
            return msg
        else:
            conn.setblocking(True)

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

    def Run(self):
        self.__server.listen() #Looks for connections
        playersInMatchmaking = []    #Empty list for client objects
        currentGames = []
        numPlayers = -1
        while True:
            if numPlayers != len(playersInMatchmaking):
                numPlayers = len(playersInMatchmaking)
            #Checks if client is trying to connect
            try:
                conn, addr = self.__server.accept() #When connection occurs
                newPlayer = Player(addr, conn)
                playersInMatchmaking.append(newPlayer)   #Appends dictionary to playersInMatchmaking list
            except socket.error:
                pass        

            #Empty list for closed sockets
            closedSockets = []

            #Creates new game object with 2 players in it 
            while len(playersInMatchmaking) >= 2:
                currentGames.append(Game(self, self, playersInMatchmaking[0], playersInMatchmaking[1]))
                closedSockets.append(playersInMatchmaking.pop(0))
                closedSockets.append(playersInMatchmaking.pop(0))
                
            #Iterates through playersInMatchmaking to check for messages
            for i in range(len(playersInMatchmaking)):
                msg = self.GetMsgs(playersInMatchmaking[i].connection, playersInMatchmaking[i].address)   #Gets message, even if " "
                #Closes connection if command given
                if msg == "!DISCONNECT":
                    closedSockets.append(playersInMatchmaking[i])
                    playersInMatchmaking[i].connection.close()   
                
                #Prints message if it isnt " "
                if msg != " " and msg != None:
                    print(f"[Message]{msg}")
                    
            #Removes closed sockets from client list
            for client in closedSockets:
                while i <= len(playersInMatchmaking) - 1:
                    if playersInMatchmaking[i].address == client.address:
                        playersInMatchmaking.pop(i)
                    else:
                        i += 1

            #Updates frame for every game currently in progress
            for game in currentGames:
                game.Run()
   
server = Server()
server.Run()