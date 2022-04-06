import pygame
import threading
from WordGeneration import WordGenerator
#For type hints
from Player import Player
from Database import DatabaseHandler

class Game:
    def __init__(self, player1 : Player, player2 : Player):
        self.started = False
        self.player1 = player1
        self.player2 = player2
        self.__dbHandler : DatabaseHandler = None
        self.__gameThread = threading.Thread(target=self.__Run)
        self.__gameThread.start()

        self.__timerStage : TimerStage = None
        self.__raceStage : Race  = None

    def __Run(self):
        #Databasehandler creates SQLITE object that can only be used in thread it was created in
        self.__dbHandler = DatabaseHandler()
        self.__timerStage = TimerStage(self.player1, self.player2)
        while not self.__timerStage.timerFinished:
            self.__timerStage.main()

        textForPlayersToType = self.__timerStage.textForPlayersToType
        self.__raceStage = Race(self.player1, self.player2, textForPlayersToType, self.__dbHandler)
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
                    player.playerQuit = True
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

        self._clock.tick()

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
    def __init__(self, player1: Player, player2: Player, textPlayersHaveToType, databaseHandler : DatabaseHandler) -> None:
        super().__init__(player1, player2)
        self.raceFinished = False
        self.__waitingForPlayersText = False
        self.timeUntilEnd = 30
        self.__timeSinceLastTimerUpdate = 0
        self.__textPlayersHaveToType = textPlayersHaveToType
        self.__player1FinalText : str = None
        self.__player2FinalText : str = None

        self.__player1TimeFinished : int = None
        self.__player2TimeFinished : int = None

        self.__dbHandler = databaseHandler

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

        #Checking if player has finished
        for player in self._players:
            if len(player.textWritten) == len(self.__textPlayersHaveToType):
                print("A player has won")

        if self.__player1FinalText is not None and self.__player2FinalText is not None:
            self._SendMessageToBothPlayers("!GAMECOMPLETED")
            self.raceFinished = True
            self.__UpdatePlayers()

    def __UpdatePlayers(self):
        #For player1
        #Calculate words typed
        self._player1.wordsTyped += len(self.__player1FinalText.split(" "))
        self._player2.wordsTyped += len(self.__player2FinalText.split(" "))

        self._player1.timePlayed += self.__player1TimeFinished
        self._player2.timePlayed += self.__player2TimeFinished

        #Find number of letters each player got correct
        player1LettersCorrect = 0
        for i in range(len(self.__player1FinalText)):
            self._player1.lettersTyped += 1
            if self.__player1FinalText[i] == self.__textPlayersHaveToType[i]:
                player1LettersCorrect += 1
                self._player1.lettersTypedCorrectly += 1

        player2LettersCorrect = 0
        for i in range(len(self.__player2FinalText)):
            self._player2.lettersTyped += 1
            if self.__player2FinalText[i] == self.__textPlayersHaveToType[i]:
                player2LettersCorrect += 1
                self._player2.lettersTypedCorrectly += 1

        #Determine winner
        #If both players wrote same number of letters correctly
        if player1LettersCorrect == player2LettersCorrect:
            if self.__player1TimeFinished == self.__player2TimeFinished:
                #Game is a draw
                winner = None
                loser = None
            elif self.__player1TimeFinished < self.__player2TimeFinished:
                winner = self._player1
                loser = self._player2
            else:
                winner = self._player2
                loser = self._player2
        elif player1LettersCorrect > player2LettersCorrect:
            winner = self._player1
            winMargin = player1LettersCorrect - player2LettersCorrect
            if winMargin > winner.largestWinMargin:
                winner.largestWinMargin = winMargin
            loser = self._player2
        else:
            winner = self._player2
            winMargin = player2LettersCorrect - player1LettersCorrect
            if winMargin > winner.largestWinMargin:
                winner.largestWinMargin = winMargin
            loser = self._player1

        if winner is not None:
            winner.msgsToSend.Enqueue("!MATCHOUTCOME:WIN")
            loser.msgsToSend.Enqueue("!MATCHOUTCOME:LOSS")

            winner.msgsToSend.Enqueue(f"!MARGIN:{winMargin}")
            loser.msgsToSend.Enqueue(f"!MARGIN:{winMargin}")

            winner.gamesWon += 1
            winner.gamesPlayed += 1
            winner.currentWinstreak += 1
            if winner.currentWinstreak > winner.longestStreak:
                winner.longestStreak = winner.currentWinstreak

            loser.gamesPlayed += 1
            loser.currentWinstreak = 0

            winner.sumOfOpponentsElo += loser.Elo
            loser.sumOfOpponentsElo += winner.Elo

            winnerGamesLost = winner.gamesPlayed - winner.gamesWon
            EloDiff = (winner.sumOfOpponentsElo + 400 * (winner.gamesWon - winnerGamesLost)) / winner.gamesPlayed - winner.Elo
            winner.msgsToSend.Enqueue(f"!ELO:{EloDiff}")
            winner.Elo += EloDiff
            if winner.Elo > winner.highestElo:
                winner.highestElo = winner.Elo

            loserGamesLost = loser.gamesPlayed - loser.gamesWon
            EloDiff = loser.Elo - (loser.sumOfOpponentsElo + 400 * (loser.gamesWon - loserGamesLost)) / loser.gamesPlayed
            loser.msgsToSend.Enqueue(f"!ELO:{EloDiff}")
            loser.Elo -= EloDiff
        else:
            self._SendMessageToBothPlayers("!MATCHOUTCOME:DRAW")

        #Updates database
        self.__dbHandler.SaveUser(self._player1)
        self.__dbHandler.SaveUser(self._player2)

        self._player1.gameFinished = True
        self._player2.gameFinished = True

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
                self.__player1TimeFinished = 30 - self.timeUntilEnd
            else:
                unusedMessages.append(message)        

        for message in unusedMessages:
            self._player1.msgsReceived.Enqueue(message)

        #For player2
        unusedMessages = []
        while self._player2.msgsReceived.GetLength() != 0:
            message = self._player2.msgsReceived.Dequeue()
            if message[:6] == "!TEXT:":
                text = message[6:]
                self._player2.textWritten = text
                self._player1.msgsToSend.Enqueue(f"!OTHERPLAYERTEXT:{self._player2.textWritten}")
            elif message[:11] == "!FINALTEXT:":
                self.__player2FinalText = message[11:]
                self.__player2TimeFinished = 30 - self.timeUntilEnd
            else:
                unusedMessages.append(message)        
        
        for message in unusedMessages:
            self._player2.msgsReceived.Enqueue(message)