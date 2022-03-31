import sqlite3
from PasswordHandling import CheckPW, GenHash
import random

#An object that will be able to handle all the operations needed related to the database
class DatabaseHandler:
    def __init__(self):
        #Connects to database 
        self.__connection = sqlite3.connect("db.db")
        self.__cursor = self.__connection.cursor()

        #Creates the tables needed if they do not exist
        command = """
        CREATE TABLE IF NOT EXISTS
        Users(
            Username TEXT PRIMARY KEY, 
            Password TEXT, 
            WordsTyped INTEGER, 
            TimePlayed INTEGER, 
            Elo INTEGER, 
            HighestElo INTEGER, 
            GamesWon INTEGER, 
            GamesPlayed INTEGER, 
            LongestStreak INTEGER, 
            LargestWinMargin FLOAT, 
            LettersTyped INTEGER,
            LettersTypedCorrectly INTEGER
            )"""
        self.__cursor.execute(command)

        command = """
        CREATE TABLE IF NOT EXISTS
        GamesPlayed(
            Username TEXT, 
            GameID INTEGER, 
            Position INTEGER, 
            TimeTaken FLOAT, 
            PRIMARY KEY(Username, GameID)
            )"""
        self.__cursor.execute(command)

        command = """
        CREATE TABLE IF NOT EXISTS
        Games(
            GameID INTEGER PRIMARY KEY, 
            Margin FLOAT)
            """
        self.__cursor.execute(command)

    def Close(self):
        self.__connection.commit()
        self.__connection.close()

    def CreateNewUser(self, username, password):
        password = GenHash(password)
        wordsTyped = 0
        timePlayed = 0
        Elo = 1000
        highestElo = 1000
        gamesWon = 0
        gamesPlayed = 0
        longestStreak = 0
        largestWinMargin = 0
        lettersTyped = 0
        lettersTypedCorrectly = 0

        params = (username, password, wordsTyped, timePlayed, Elo, highestElo, gamesWon, gamesPlayed, longestStreak, largestWinMargin, lettersTyped, lettersTypedCorrectly)
        command = """
        INSERT INTO Users
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        self.__cursor.execute(command, params)

    def CreateRandomUser(self, username, password):
        password = GenHash("Password" + str(password))
        wordsTyped = random.randint(0,1000000)
        timePlayed = random.randint(0,999999999)
        Elo = random.randint(500, 4000)
        highestElo = random.randint(Elo, Elo + 200)
        gamesPlayed = random.randint(0, 100000)
        gamesWon = random.randint(0, gamesPlayed)
        longestStreak = random.randint(0, gamesWon)
        largestWinMargin = random.randint(0, 100)
        lettersTyped = random.randint(0, 99999999999999)
        lettersTypedCorrectly = random.randint(0, lettersTyped)

        params = (username, password, wordsTyped, timePlayed, Elo, highestElo, gamesWon, gamesPlayed, longestStreak, largestWinMargin, lettersTyped, lettersTypedCorrectly)
        command = """
        INSERT INTO Users
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        self.__cursor.execute(command, params)

    def CheckIfUsernameInDB(self, username):
        params = (username,)
        command = """SELECT * FROM Users WHERE Username = ?"""

        self.__cursor.execute(command, params)
        if self.__cursor.fetchall() == []:
            return False

        else:
            return True
            
    def CheckPassword(self, username, password):
        params = (username,)
        command = """
        SELECT Password FROM Users 
        WHERE Username = (?)
        """
        self.__cursor.execute(command, params)
        fetchResult = self.__cursor.fetchall()
        correctPasswordHash = fetchResult[0][0]

        #Uses bcrypt library to check password against hash
        if CheckPW(password, correctPasswordHash):
            return True
        return False


# dbHandler = DatabaseHandler()

# # thisPlayer = Player(0,0)
# # thisPlayer.username = "Player0"

# # thisPlayer = dbHandler.LoadUser(thisPlayer)

# # for i in range(50,60):
# #     dbHandler.CreateRandomUser(f"Username{i}", f"Password{i}")

# for i in range(50):
#     print(dbHandler.CheckPassword("Username" + str(i), "Password" + str(i)))

# dbHandler.Close()