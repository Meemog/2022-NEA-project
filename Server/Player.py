class Player:
    def __init__(self, address, connection):
        self.address = address
        self.connection = connection
        self.msgsToSend = []
        self.msgsReceived = []

        #Details used for stats section and logging in / creating new player
        self.username = ""
        self.password = ""
        self.level = 0
        self.avgWPM = 0
        self.Elo = 1000
        self.highestElo = 1000
        self.gamesWon = 0
        self.gamesPlayed = 0
        self.longestStreak = 0
        self.largestWinMargin = 0
        self.accuracy = 0

    def SendMsg(self, msg):
        self.msgsToSend.append(msg)