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
        print(self.__backText)
    
    def Run(self):
        startTimer = 0
        #Sends background text to players
        if not self.started:
            print("Got to game countdown")
            msg = f"BACKTEXT:{self.__backText}"
            self.__server.SendMsg(msg, self.__1player.connection)
            self.__server.SendMsg(msg, self.__2player.connection)
            self.started = True

            #Timer for game starting
        # while not self.started:
        #     self.__clock.tick()
        #     startTimer += self.__clock.get_time()
        #     if startTimer % 1000 == 0:
        #         msg = f"!SECONDSLEFTUNTILSTART:{startTimer/1000}"
        #         self.__server.SendMsg(msg, self.__1player.connection)
        #         self.__server.SendMsg(msg, self.__2player.connection)

        #     if startTimer / 1000 == self.__delayBeforeStart:
        #         self.started = True

        # while self.__running:
        #     pass


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