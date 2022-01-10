import pygame
from WordGeneration import WordGenerator

class Game:
    def __init__(self, serverSocket, server, player1, player2):
        self.__1player = player1
        self.__2player = player2
        self.__server = server
        self.__clock = pygame.time.Clock()  #Pygame clock object
        self.started = False
        self.__delayBeforeStart = 3 #Seconds before game starts
        self.__timeInGame = 30      #Seconds before game ends
        self.__running = True
        self.__disconnected = ""
        self.__backText = WordGenerator().GetWordsForProgram(500)
    
    def Run(self):
        #Time before game starts in seconds
        startTimer = 5
        #Starts the countdown for the clients
        self.__Countdown(startTimer)
        self.__SendBackgroundText()
        self.started = True

    def __SendBackgroundText(self):
        print("Got to game countdown")
        msg = f"BACKTEXT:{self.__backText}"
        self.__SendMsgToBothPlayers(msg)

    #This method counts down from timer seconds and updates the client on this
    def __Countdown(self, timer):
        #Used to detect when the timer should be sent to client
        timeSinceLastMessage = 1000 #milliseconds
        started = False

        #Waits until the timer has run out
        while not started:
            self.__clock.tick()
            timeSinceLastMessage += self.__clock.get_time()
            #Checks if 1 second has passed since last message and sends the seconds left to both clients
            if timeSinceLastMessage >= 1000:
                msg = f"!SECONDSLEFTUNTILSTART:{timer}"
                self.__SendMsgToBothPlayers(msg)
                timer -= 1
                timeSinceLastMessage -= 1000
            #If the time has run out
            if timer == 0:
                started = True

    #Sends the same message to both players
    def __SendMsgToBothPlayers(self, msg):
        self.__server.SendMsg(msg, self.__1player.connection)
        self.__server.SendMsg(msg, self.__2player.connection)

    def CheckMsgs(self):
        #Check for messages from player 1
        msg = self.__server.GetMsgs(self.__1player.connection, self.__1player.address)
        if msg == " ":
            pass

        elif msg == "!DISCONNECT":
            self.__running = False
            self.__disconnected = "player1"

        elif msg[:8] == "!LETTER:":
            self.__server.SendMsg(msg[8:], self.__1player.connection)

        #Checks for messages from player 2
        msg = self.__server.GetMsgs(self.__2player.connection, self.__2player.address)
        if msg == " ":
            pass

        elif msg == "!DISCONNECT":
            self.__running = False
            self.__disconnected = "player1"

        elif msg[:8] == "!LETTER:":
            self.__server.SendMsg(msg[8:], self.__2player.connection)