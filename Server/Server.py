import socket
from Game import Game
from Player import Player
from Database import DatabaseHandler

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
        self.__dbHandler = DatabaseHandler()
        print("[SERVER STARTED]")

    #Made to be used in a seperate thread
    #Checks each player for a message being sent
    #If a message is received it is appended to the list player.msgsReceived
    def GetMsgs(self, players):
        for player in players:
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
                print(f"Message Received:{msg}")

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
                    print(f"Message sent:{msg}")
                player.msgsToSend = []
            except socket.error:
                pass
            player.connection.setblocking(True)

    #Function to be used in the run function to look for new players and not block everything else that needs to happen
    #Ran in parallel by using threading module
    def __CheckForNewPlayers(self):
        self.__server.setblocking(False)
        try:        
            conn, addr = self.__server.accept() #When connection occurs
            thisPlayer = Player(addr, conn)
            self.players.append(thisPlayer)
        except:
            pass
        self.__server.setblocking(True)

    def __PrintPlayersInMatchmaking(self):#
        print(f"Players:{len(self.players)}, in matchmaking:{len(self.playersInMatchmaking)}", end="\r")

    def __CreateNewGame(self):
        self.currentGames.append(Game(self.playersInMatchmaking[0], self.playersInMatchmaking[1]))
        self.players.append(self.playersInMatchmaking.pop(0))
        self.players.append(self.playersInMatchmaking.pop(0))
        self.currentGames[-1].StartThread()

    #Goes through every message for every player in players parameter
    def __HandleMessages(self):
        i = 0
        while i < len(self.players):
            while self.players != [] and self.players[i].msgsReceived != []:
                if self.players[i].msgsReceived[0] == "!DISCONNECT":
                    self.players[i].msgsReceived = []
                    self.players.pop(i)
                    i -= 1

                elif self.players[i].msgsReceived[0] == "!QUEUE":
                    self.players[i].msgsReceived.pop(0)
                    self.playersInMatchmaking.append(self.players.pop(i))
                    i -= 1
                    
                #Checks if players login details are correct
                elif not self.players[i].loggedIn and self.players[i].msgsReceived[0][:7] == "!LOGIN:":
                    details = self.players[i].msgsReceived.pop(0)[7:]
                    details = details.split(",")
                    username = details[0]
                    password = details[1]

                    if self.__dbHandler.CheckIfUsernameInDB(username):
                        self.players[i].username = username
                        correctPassword = self.__dbHandler.GetPassword(username)
                        if password == correctPassword:
                            self.players[i].SendMsg("!PASSWORDCORRECT")
                            self.__dbHandler.LoadUser(self.players[i])
                        else:
                            self.players[i].SendMsg("!PASSWORDINCORRECT")
                    
                    else:
                        self.players[i].SendMsg("!USERNAMENOTFOUND")

                elif self.players[i].username == "" and self.players[i].msgsReceived[0][:10] == "!REGISTER:":
                    details = self.players[i].msgsReceived[0][10:]
                    details = details.split(",")
                    self.players[i].username = details[0]
                    self.players[i].password = details[1]
                    #Creates new user in database
                    self.__dbHandler.CreateNewUser(self.players[i])

                    self.players[i].msgsReceived.pop(0)

                else:
                    self.players[i].msgsReceived.pop(0)
            i += 1
            
        i = 0
        while i < len(self.playersInMatchmaking):
            while self.playersInMatchmaking[i] != [] and self.playersInMatchmaking[i].msgsReceived != []:
                if self.playersInMatchmaking[i].msgsReceived[0] == "!DISCONNECT":
                    self.playersInMatchmaking[i].msgsReceived = []
                    self.playersInMatchmaking.pop(i)
                    i -= 1

                elif self.playersInMatchmaking[i].msgsReceived[0] == "!DEQUEUE":
                    self.playersInMatchmaking[i].msgsReceived.pop(0)
                    self.players.append(self.playersInMatchmaking.pop(0))
                    i -= 1
                    
                #More messages can be handled here

                #Checks if players login details are correct
                elif self.playersInMatchmaking[i].username != "" and self.playersInMatchmaking[i].msgsReceived[0][:7] == "!LOGIN:":
                    details = self.playersInMatchmaking[i].msgsReceived[0][7:]
                    details = details.split(",")
                    username = details[0]
                    password = details[1]
                    correctUsername = "TestUsername"
                    correctPassword = "TestPassword"
                    if username == correctUsername and password == correctPassword:
                        self.playersInMatchmaking[i].SendMsg("!PASSWORDCORRECT")
                        self.playersInMatchmaking[i].username = username
                    else:
                        self.playersInMatchmaking[i].SendMsg("!PASSWORDINCORRECT")

                    self.playersInMatchmaking[i].msgsReceived.pop(0)

                else:
                    self.playersInMatchmaking[i].msgsReceived.pop(0)
            i += 1

    def Run(self):
        self.__server.listen() #Looks for connections
        self.currentGames = []
        while self.running:
            self.__CheckForNewPlayers()
            #Prints players in matchmaking
            self.__PrintPlayersInMatchmaking()

            #Creates new game object with 2 players in it 
            while len(self.playersInMatchmaking) >= 2:
                self.__CreateNewGame()
                
            self.GetMsgs(self.players)
            self.GetMsgs(self.playersInMatchmaking)
            self.SendMsgs()
            self.__HandleMessages()

server = Server()
server.Run()
