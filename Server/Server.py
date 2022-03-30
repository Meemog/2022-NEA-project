import socket
from Game import Game
from Player import Player
from Database import DatabaseHandler

class Server:
    def __init__(self):
        self.HEADER = 8
        self.PORT = 5000
        self.SERVER = socket.gethostbyname(socket.gethostname()) #Gets the local IP address
        self.ADDRESS = (self.SERVER, self.PORT) #Makes a tuple for the address
        self.FORMAT = 'utf-8'

        self.running = True
        self.players = []
        self.playersInMatchmaking = []
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET is for ipv4. SOCK_STREAM is for TCP, SOCK_DGRAM is UDP
        self.server.bind(self.ADDRESS)
        self.dbHandler = DatabaseHandler()
        print("[SERVER STARTED]")

    #Made to be used in a seperate thread
    #Checks each player for a message being sent
    #If a message is received it is appended to the list player.msgsReceived
    def GetMsgs(self, players):
        for player in players:
            player.connection.setblocking(False)
            try:
                msgLen = int(player.connection.recv(self.HEADER).decode(self.FORMAT)) #Waits for message with length 8 bytes to be received from the client and then decodes it 
            except:
                player.connection.setblocking(True)
                return 0
            player.connection.setblocking(True)
            if msgLen > 0:  #First message will always be empty
                msg = player.connection.recv(msgLen).decode(self.FORMAT) #Waits for a message with length msgLen to be received
                player.msgsReceived.append(msg)       
                print(f"Message Received:{msg}")

    #Made to be used in a seperate thread
    #Checks each player for a message that needs to be sent from player.msgsToSend list
    #If a message needs to be sent it will send it and remove it from the list
    def SendMsgsToPlayersNotInQueue(self):
        #Checks queue for each player to send messages that need to be sent.
        for player in self.players:
            player.connection.setblocking(False)
            while player.msgsToSend.GetLength() != 0:
                message = player.msgsToSend.Dequeue()
                try:
                    conn = player.connection
                    encMessage = message.encode(self.FORMAT) #encodes msg with utf-8
                    msgLen = len(encMessage)
                    msgLen = str(msgLen).encode(self.FORMAT) 
                    msgLen += b' ' * (self.HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
                    #b' ' means the byte representation of a space
                    conn.send(msgLen)
                    conn.send(encMessage)
                except socket.error:
                    player.msgsToSend.Enqueue(message)
            player.connection.setblocking(True)

    def SendMsgsToPlayersInQueue(self):
        #Checks queue for each player to send messages that need to be sent.
        for player in self.playersInMatchmaking:
            player.connection.setblocking(False)
            while player.msgsToSend.GetLength() != 0:
                message = player.msgsToSend.Dequeue()
                try:
                    conn = player.connection
                    encMessage = message.encode(self.FORMAT) #encodes msg with utf-8
                    msgLen = len(encMessage)
                    msgLen = str(msgLen).encode(self.FORMAT) 
                    msgLen += b' ' * (self.HEADER - len(msgLen)) #makes the message length be 8 bytes long so the server recognises it
                    #b' ' means the byte representation of a space
                    conn.send(msgLen)
                    conn.send(encMessage)
                except socket.error:
                    player.msgsToSend.Enqueue(message)
            player.connection.setblocking(True)

    #Function to be used in the run function to look for new players and not block everything else that needs to happen
    #Ran in parallel by using threading module
    def CheckForNewPlayers(self):
        self.server.setblocking(False)
        try:        
            conn, addr = self.server.accept() #When connection occurs
            thisPlayer = Player(addr, conn)
            self.players.append(thisPlayer)
        except:
            pass
        self.server.setblocking(True)

    def PrintPlayers(self):#
        print(f"Players:{len(self.players)}, in matchmaking:{len(self.playersInMatchmaking)}", end="\r")

    def HandleMessagesForPlayersNotInQueue(self):
        playersQuit = []
        for player in self.players:
            while player.msgsReceived.GetLength() != 0:
                message = player.msgsReceived.Dequeue()
                if player.loggedIn and message == "!DISCONNECT":
                    playersQuit.append(player)
                
                elif player.loggedIn and message == "!QUEUE":
                    playersQuit.append(player)
                    self.playersInMatchmaking.append(player)

                elif not player.loggedIn and message[:7] == "!LOGIN:":
                    details = message[7:].split(",")
                    username = details[0]
                    password = details[1]

                    #Checks password and sends message to user to confirm if they are signed in or not
                    if self.dbHandler.CheckIfUsernameInDB(username):
                        if self.dbHandler.CheckPassword(username, password):
                            player.loggedIn = True
                            player.msgsToSend.Enqueue("!PASSWORDCORRECT")
                        else:
                            player.msgsToSend.Enqueue("!PASSWORDINCORRECT")
                    else:
                        player.msgsToSend.Enqueue("!USERNAMENOTFOUND")
                
        #Removes players who quit from the list of players
        playersRemoved = 0
        for player in playersQuit:
            for i in range(len(self.players)):
                if player == self.players[i - playersRemoved]:
                    playersRemoved += 1
                    self.players.pop(i - playersRemoved)

    def HandleMessagesForPlayersInQueue(self):
        playersQuit = []
        for player in self.playersInMatchmaking:
            while player.msgsReceived.GetLength() != 0:
                message = player.msgsReceived.Dequeue()
                if message == "!DISCONNECT":
                    playersQuit.append(player)
                elif message == "!DEQUEUE":
                    playersQuit.append(player)
                    self.players.append(player)
        
        playersRemoved = 0
        for player in playersQuit:
            for i in range(len(self.playersInMatchmaking)):
                if player == self.playersInMatchmaking[i - playersRemoved]:
                    playersRemoved += 1
                    self.playersInMatchmaking.pop(i - playersRemoved)

    def Run(self):
        self.server.listen() #Looks for connections
        self.currentGames = []
        while self.running:
            self.CheckForNewPlayers()
            self.PrintPlayers()

            #Handling messages
            self.GetMsgs(self.players)
            self.HandleMessagesForPlayersNotInQueue()
            self.SendMsgsToPlayersNotInQueue()

            self.GetMsgs(self.playersInMatchmaking)
            self.HandleMessagesForPlayersInQueue()
            self.SendMsgsToPlayersInQueue()

server = Server()
server.Run()
