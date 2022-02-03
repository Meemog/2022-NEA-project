import socket
from Game import Game
from Player import Player

class Server:
    def __init__(self):
        self.__HEADER = 8
        self.__PORT = 5000
        self.__SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
        self.__ADDRESS = (self.__SERVER, self.__PORT) #Makes a tuple for the address
        self.__FORMAT = 'utf-8'
        self.players = []
        self.playersInMatchmaking = []
        self.running = True #Boolean used to close other threads once the program ends

        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
        self.__server.bind(self.__ADDRESS)
        print("[SERVER STARTED]")

    #Made to be used in a seperate thread
    #Checks each player for a message being sent
    #If a message is received it is appended to the list player.msgsReceived
    def GetMsgs(self):
        for player in self.players:
            player.connection.setblocking(False)
            try:
                msgLen = int(player.connection.recv(self.__HEADER).decode(self.__FORMAT)) #Waits for message with length 8 bytes to be received from the client and then decodes it 
            except:
                player.connection.setblocking(True)
                return 0
            player.connection.setblocking(True)
            if msgLen > 0:  #First message will always be empty
                msg = player.connection.recv(msgLen).decode(self.__FORMAT) #Waits for a message with length msgLen to be received
                player.msgsReceived.append(msg)       

    #Made to be used in a seperate thread
    #Checks each player for a message that needs to be sent from player.msgsToSend list
    #If a message needs to be sent it will send it and remove it from the list
    def SendMsgs(self):
        #Checks queue for each player to send messages that need to be sent.
        for player in self.players:
            player.connection.setblocking(False)
            try:
                for msg in player.msgsToSend:
                    conn = player.connection
                    encMessage = msg.encode(self.__FORMAT) #encodes msg with utf-8
                    msgLen = len(encMessage)
                    msgLen = str(msgLen).encode(self.__FORMAT) 
                    msgLen += b' ' * (self.__HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
                    #b' ' means the byte representation of a space
                    conn.send(msgLen)
                    conn.send(encMessage)
            except socket.error:
                pass
            player.connection.setblocking(True)
        return 0

    #Function to be used in the run function to look for new players and not block everything else that needs to happen
    #Ran in parallel by using threading module
    def __CheckForNewPlayers(self):
        self.__server.setblocking(False)
        try:        
            conn, addr = self.__server.accept() #When connection occurs
            thisPlayer = Player(addr, conn)
            self.playersInMatchmaking.append(thisPlayer)   #Appends player object to self.players list
            self.players.append(thisPlayer)
            self.hasPrintedNewPlayers = False
        except:
            pass
        self.__server.setblocking(True)

    def __PrintPlayersInMatchmaking(self):
        print('-'*80)
        for player in self.playersInMatchmaking:
            print(f"[Player]{player}")
        print('-'*80)
        self.hasPrintedNewPlayers = True

    def __CreateNewGame(self):
        self.currentGames.append(Game(self, self.playersInMatchmaking[0], self.playersInMatchmaking[1]))
        self.playersInMatchmaking.pop(0)
        self.playersInMatchmaking.pop(0)
        self.currentGames[-1].StartThread()
        self.hasPrintedNewPlayers = False

    def __CheckIfPlayersQuit(self):
        disconnectedPlayers = []
        #Iterates through self.playersInMatchmaking to check for messages
        for i in range(len(self.playersInMatchmaking)):
            for msg in self.playersInMatchmaking[i].msgsReceived:
                #Closes connection if command given
                if msg == "!DISCONNECT":
                    disconnectedPlayers.append(i)
                    i -= 1
                    self.hasPrintedNewPlayers = False
                #Prints message on server console
                print(f"[Message{str(self.playersInMatchmaking[i].address)}]{msg}")
            self.playersInMatchmaking[i].msgsReceived = []

        while len(disconnectedPlayers) > 0:
            self.playersInMatchmaking.pop(disconnectedPlayers[-1])
            disconnectedPlayers.pop(-1)

    def Run(self):
        self.__server.listen() #Looks for connections
        self.currentGames = []
        self.hasPrintedNewPlayers = False
        while self.running:
            self.__CheckForNewPlayers()
            #Prints players in matchmaking
            if not self.hasPrintedNewPlayers:
                self.__PrintPlayersInMatchmaking()

            #Creates new game object with 2 players in it 
            while len(self.playersInMatchmaking) >= 2:
                self.__CreateNewGame()
                
            self.GetMsgs()
            self.SendMsgs()
            self.__CheckIfPlayersQuit()

server = Server()
server.Run()
