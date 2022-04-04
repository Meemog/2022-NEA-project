from Datastructures import Queue

class Player:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.connected = True
        self.msgsToSend = Queue()
        self.msgsReceived = Queue()
        self.loggedIn = False

        self.username = ""
        self.wordsTyped = 0
        self.timePlayed = 0
        self.Elo = 0
        self.highestElo = 0
        self.gamesWon = 0
        self.gamesPlayed = 0
        self.longestStreak = 0
        self.largestWinMargin = 0
        self.lettersTyped = 0
        self.lettersTypedCorrectly = 0

        self.textWritten = ""

    def Reset(self):
        self.textWritten = ""
    