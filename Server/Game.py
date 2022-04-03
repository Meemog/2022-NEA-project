import pygame
import threading
from WordGeneration import WordGenerator
#For type hints
from Player import Player

class Game:
    def __init__(self, player1 : Player, player2 : Player):
        self.started = False
        self.player1 = player1
        self.player2 = player2
        self.__gameThread = threading.Thread(target=self.__Run)
        self.__gameThread.start()

    def __Run(self):
        self.__timerStage = TimerStage(self.player1, self.player2)
        while not self.__timerStage.timerFinished:
            self.__timerStage.main()

        textForPlayersToType = self.__timerStage.textForPlayersToType
        self.__raceStage = Race(self.player1, self.player2, textForPlayersToType)
        #Runs racestage when the race is ongoing
        while not self.__raceStage.raceFinished:
            self.__raceStage.main()

class Stage:
    def __init__(self, player1 : Player, player2 : Player) -> None:
        self._clock = pygame.time.Clock()
        self._player1 = player1
        self._player2 = player2
        self._players = [self._player1, self._player2]

    def main(self):
        self._clock.tick()
        self._HandleMessages()

    def _HandleMessages(self):
        for player in self._players:
            unusedMessages = []
            while player.msgsReceived.GetLength() != 0:
                message = player.msgsReceived.Dequeue()
                if message == "!DISCONNECT":
                    player.connected = False
                    #TODO implement abandon penalty
                else:
                    unusedMessages.append(message)

            for message in unusedMessages:
                player.msgsReceived.Enqueue(message)

    def _SendMessageToBothPlayers(self, messageToSend):
        self._player1.msgsToSend.Enqueue(messageToSend)
        self._player2.msgsToSend.Enqueue(messageToSend)

#Stage for when players are waiting for game to start
class TimerStage(Stage):
    def __init__(self, player1 : Player, player2 : Player) -> None:
        super().__init__(player1, player2)
        self.timerFinished = False
        #Attribute for timer in seconds
        self.timeUntilStart = 5
        self.__timeSinceLastMessage = 0
        self._SendMessageToBothPlayers("!STARTTIMER")
        self._SendMessageToBothPlayers(f"!TIMELEFT:{self.timeUntilStart}")

        #Word generation
        self.__wordGenerator = WordGenerator()
        self.textForPlayersToType = self.__wordGenerator.GetWordsForProgram(500)

    #Runs every frame in Game.main() while timerfinished is false
    def main(self):
        super().main()
        self.__timeSinceLastMessage += self._clock.get_time()
        if self.timeUntilStart == 0:
            self.timerFinished = True
            self._SendMessageToBothPlayers(f"!TEXTTOWRITE:{self.textForPlayersToType}")
        elif self.__timeSinceLastMessage >= 1000:
            self.__timeSinceLastMessage -= 1000
            self.timeUntilStart -= 1
            self._SendMessageToBothPlayers(f"!TIMELEFT:{self.timeUntilStart}")

class Race(Stage):
    def __init__(self, player1: Player, player2: Player, textPlayersHaveToType) -> None:
        super().__init__(player1, player2)
        self.raceFinished = False
        self.__waitingForPlayersText = False
        self.timeUntilEnd = 30
        self.__timeSinceLastTimerUpdate = 0
        self.__textPlayersHaveToType = textPlayersHaveToType
        self.__player1FinalText : str = None
        self.__player2FinalText : str = None

    def main(self):
        super().main()

        self.__timeSinceLastTimerUpdate += self._clock.get_time()
        if self.__timeSinceLastTimerUpdate >= 1000 and not self.__waitingForPlayersText:
            self.timeUntilEnd -= 1
            self.__timeSinceLastTimerUpdate -= 1000
            self._SendMessageToBothPlayers(f"!TIMELEFT:{self.timeUntilEnd}")
            if self.timeUntilEnd == 0:
                self._SendMessageToBothPlayers("!GAMECOMPLETE")
                self.__waitingForPlayersText = True

        if self.__player1FinalText is not None and self.__player2FinalText is not None:
            self._SendMessageToBothPlayers("!GAMECOMPLETED")
            self.raceFinished = True

        #Checking if player has finished
        for player in self._players:
            if len(player.textWritten) == len(self.__textPlayersHaveToType):
                #TODO player finished
                print("A player has won")

    def _HandleMessages(self):
        super()._HandleMessages()

        #For player1
        unusedMessages = []
        while self._player1.msgsReceived.GetLength() != 0:
            message = self._player1.msgsReceived.Dequeue()
            if message[:6] == "!TEXT:":
                text = message[6:]
                self._player1.textWritten = text
                self._player2.msgsToSend.Enqueue(f"!OTHERPLAYERTEXT:{self._player1.textWritten}")
            elif message[:11] == "!FINALTEXT:":
                self.__player1FinalText = message[11:]
            else:
                unusedMessages.append(message)        
        
        for message in unusedMessages:
            self._player1.msgsReceived.Enqueue(message)

        unusedMessages = []
        #For player2
        while self._player2.msgsReceived.GetLength() != 0:
            message = self._player2.msgsReceived.Dequeue()
            if message[:6] == "!TEXT:":
                text = message[6:]
                self._player2.textWritten = text
                self._player2.msgsToSend.Enqueue(f"!OTHERPLAYERTEXT:{self._player2.textWritten}")
            elif message[:11] == "!FINALTEXT:":
                self.__player2FinalText = message[11:]
            else:
                unusedMessages.append(message)        
        
        for message in unusedMessages:
            self._player2.msgsReceived.Enqueue(message)