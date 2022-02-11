import sqlite3
from Player import Player

#An object that will be able to handle all the operations needed related to the database
class DatabaseHandler:
    def __init__(self):
        #Connects to database 
        self.__connection = sqlite3.connect("db.db")
        self.__cursor = self.__connection.cursor()

        #Creates the tables needed if they do not exist
        command = """CREATE TABLE IF NOT EXISTS
        Users(Username TEXT PRIMARY KEY, Level INTEGER, Password TEXT, AverageWPM FLOAT, Elo INTEGER, HighestElo INTEGER, GamesWon INTEGER, GamesPlayed INTEGER, LongestStreak INTEGER, LargestWinMargin FLOAT, Accuracy FLOAT)"""
        self.__cursor.execute(command)
        command = """CREATE TABLE IF NOT EXISTS
        GamesPlayed(Username TEXT, GameID INTEGER, Position INTEGER, TimeTaken FLOAT, PRIMARY KEY(Username, GameID))"""
        self.__cursor.execute(command)
        command = """CREATE TABLE IF NOT EXISTS
        Games(GameID INTEGER PRIMARY KEY, Margin FLOAT)"""
        self.__cursor.execute(command)

    def Close(self):
        self.__connection.commit()
        self.__connection.close()

    def CreateNewUser(self, player):
        username = player.username
        password = player.password
        level = player.level
        avgWPM = player.avgWPM
        Elo = player.Elo
        highestElo = player.highestElo
        gamesWon = player.gamesWon
        gamesPlayed = player.gamesPlayed
        longestStreak = player.longestStreak
        largestWinMargin = player.largestWinMargin
        accuracy = player.accuracy

        params = (username, level, password, avgWPM, Elo, highestElo, gamesWon, gamesPlayed, longestStreak, largestWinMargin, accuracy)

        command = """INSERT INTO Users
        VALUES(?,?,?,?,?,?,?,?,?,?,?)"""

        self.__cursor.execute(command, params)

    def CheckIfUsernameInDB(self, username):
        params = (username,)
        command = """SELECT * FROM Users WHERE Username = ?"""

        self.__cursor.execute(command, params)
        if self.__cursor.fetchall() == []:
            return False

        else:
            return True
            
    def GetPassword(self, username):
        params = (username,)
        command = """SELECT Password FROM Users WHERE Username = ?"""

        self.__cursor.execute(command, params)
        password = self.__cursor.fetchall()[0][0]
        return password

    #Takes player object with username already defined and returns player object with values from database
    def LoadUser(self, player):
        params = (player.username,)
        command = "SELECT * FROM Users WHERE Username = (?)"
        self.__cursor.execute(command, params)
        valuesReturned = self.__cursor.fetchall()   #Gives a list of tuples with the correct values in them
        print(valuesReturned)
        valuesReturned = valuesReturned[0]
        player.username = valuesReturned[0]
        player.level = valuesReturned[1]
        player.avgWPM = valuesReturned[3]
        player.Elo = valuesReturned[4]
        player.highestElo = valuesReturned[5]
        player.gamesWon = valuesReturned[6]
        player.gamesPlayed = valuesReturned[7]
        player.longestStreak = valuesReturned[8]
        player.largestWinMargin = valuesReturned[9]
        player.accuracy = valuesReturned[10]

        return player

# dbHandler = DatabaseHandler()

# # thisPlayer = Player(0,0)
# # thisPlayer.username = "Player0"

# # thisPlayer = dbHandler.LoadUser(thisPlayer)

# player = Player(0,0)
# player.username = "Player0"
# print(dbHandler.LoadUser(player))

# dbHandler.Close()