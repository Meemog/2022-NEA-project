import pygame
import threading
from WordGeneration import WordGenerator

class Game:
    def __init__(self, server, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.__server = server
        self.__clock = pygame.time.Clock()  #Pygame clock object
        self.started = False
        self.__backTextSent = False
        self.__timerSent = False
        self.__delayBeforeStart = 5 #Seconds before game starts
        self.__timeInGame = 30      #Seconds before game ends
        self.__running = True
        self.__disconnected = ""
        self.__timeSinceLastMessage = 1000 #milliseconds
        self.__gameThread = threading.Thread(target=self.__Run)
        print("Game init")
    
    def StartThread(self):
        self.__gameThread.start()

    def __Run(self):
        self.__backText = WordGenerator().GetWordsForProgram(500)
        #Main Loop for the game
        while self.__running:
            self.__clock.tick()
            if not self.started:
                #Manages countdown for clients
                self.__Countdown()
            #Sends background text if game has started but only does this once
            elif not self.__backTextSent and self.started:
                self.__SendBackgroundText()

            #Checks messages of both players
            self.CheckMsgs()
    
        #End of game
        if self.__disconnected != "":
            if self.__disconnected == "player1":
                pass
                #Do something when player 1 has disconnected

            else:
                pass
                #Do something when player 2 has disconnected

        else:
            pass
            #Do something when the game ended normally

    def __SendBackgroundText(self):
        print("Got to game countdown")
        msg = f"!BACKTEXT:{self.__backText}"
        self.__SendMsgToBothPlayers(msg)
        self.__backTextSent = True

    #This method counts down from timer seconds and updates the client on this
    def __Countdown(self):
        if not self.__timerSent:
            #Sends message to clients to start timer
            msg = f"!SECONDSLEFTUNTILSTART:{self.__delayBeforeStart}"
            self.__SendMsgToBothPlayers(msg)
            self.__delayBeforeStart *= 1000
            self.__timerSent = True

        #Waits until the timer has run out
        self.__delayBeforeStart -= self.__clock.get_time()

        #If the time has run out
        if self.__delayBeforeStart <= 0:
            self.started = True

    #Sends the same message to both players
    def __SendMsgToBothPlayers(self, msg):
        self.player1.SendMsg(msg)
        self.player2.SendMsg(msg)

    def CheckMsgs(self):
        for msg in self.player1.msgsReceived:
            if msg == " ":
                pass

            elif msg == "!DISCONNECT":
                self.__running = False
                self.__disconnected = "player1"

            elif msg[:8] == "!LETTER:":
                #Do things with letter
                pass

        for msg in self.player2.msgsReceived:
            if msg == " ":
                pass

            elif msg == "!DISCONNECT":
                self.__running = False
                self.__disconnected = "player2"

            elif msg[:8] == "!LETTER:":
                #Do things with letter
                pass