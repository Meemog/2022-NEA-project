import pygame
import threading
from WordGeneration import WordGenerator

class Game:
    def __init__(self, player1, player2):
        self.started = False
        self.player1 = player1
        self.player2 = player2
        self.__gameThread = threading.Thread(target=self.__Run)
        self.__gameThread.start()

    def __Run(self):
        self.__timerStage = TimerStage(self.player1, self.player2)
        while not self.__timerStage.timerFinished:
            self.__timerStage.main()

class Stage:
    def __init__(self, player1, player2) -> None:
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
                else:
                    unusedMessages.append(message)

            for message in unusedMessages:
                player.msgsReceived.Enqueue(message)

    def _SendMessageToBothPlayers(self, messageToSend):
        self._player1.msgsToSend.Enqueue(messageToSend)
        self._player2.msgsToSend.Enqueue(messageToSend)

#Stage for when players are waiting for game to start
class TimerStage(Stage):
    def __init__(self, player1, player2) -> None:
        super().__init__(player1, player2)
        self.timerFinished = False
        #Attribute for timer in seconds
        self.__timeUntilStart = 5
        self.__timeSinceLastMessage = 0
        self._SendMessageToBothPlayers("!STAGE:TIMER")
        self._SendMessageToBothPlayers(f"!TIMELEFT:{self.__timeUntilStart}")

    #Runs every frame in Game.main() while timerfinished is false
    def main(self):
        super().main()
        self.__timeSinceLastMessage += self._clock.get_time()
        if self.__timeUntilStart == 0:
            self.timerFinished = True
        elif self.__timeSinceLastMessage >= 1000:
            self.__timeSinceLastMessage -= 1000
            self.__timeUntilStart -= 1
            self._SendMessageToBothPlayers(f"!TIMELEFT:{self.__timeUntilStart}")