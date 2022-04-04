import pygame, threading
from Scene import Scene, ConnectionScreen, LoginScreen, MainMenu, MatchmakingScreen, TimerScene, RaceScene, PostGame

class Game:
    def __init__(self, window):
        self.socket = None
        self.__loggedIn = False
        self.__window = window
        self.__userQuit = False

        #Temporary variable which will be set once the socket is connected
        self.__socketHandleThread = None

        self.__resolution = pygame.display.Info()
        self.__resolution = (self.__resolution.current_w / 1920, self.__resolution.current_h / 1080)

        self.__connectionScreen : ConnectionScreen = None
        self.__loginScreen : LoginScreen = None
        self.__mainMenu : MainMenu = None
        self.__matchmakingScreen : MatchmakingScreen = None
        self.__timerScene : TimerScene = None
        self.__raceScene : RaceScene = None
        self.__postGameScreen : PostGame = None

        self.__timerStarted = False
        self.__textToWrite = None
        self.__matchResults = None

    def main(self):
        #Connects to server
        self.ConnectToServer()
        #I couldn't come up with a more readable solution for having to end the game after any of these scenes than to simply check after every one
        #I previously had a solution with an activescene attribute but that was unreadable and provided no real benefit
        if self.__userQuit:
            return 0

        #Goes to loginscreen
        self.Login()
        if self.__userQuit:
            return 0

        #Main loop where player goes to main menu and back#
        while True:
            self.__mainMenu = MainMenu(self.__window, self.__resolution, self.socket)
            self.__matchmakingScreen = MatchmakingScreen(self.__window, self.__resolution, self.socket)
            self.__timerScene = TimerScene(self.__window, self.__resolution, self.socket)
            self.__timerStarted = False
            self.__textToWrite = None
            self.__results = None
            self.__margin = None
            self.__ELodiff = None

            #Goes to main menu to get choice from user
            self.GetChoiceFromUser()
            if self.__userQuit:
                return 0
            userChoice = self.__mainMenu.userChoice

            if userChoice == "Play":
                #Goes to matchmaking screen
                self.WaitForGame()
                #If user quit during matchmaking
                #Disconnecting from server is done in Play.py
                #If the user disconnects from server while in queue, server will automatically dequeue them
                if self.__userQuit:
                    return 0
                #If user left queue
                elif self.__matchmakingScreen.userClickedBackButton:
                    self.socket.msgsToSend.append("!DEQUEUE")
                    #Loop starts again and user goes to main menu
                #If game was found
                elif self.__matchmakingScreen.gameFound:
                    self.PreGameTimer()
                    if self.__userQuit:
                        return 0
                    #Waits for previewtext from server
                    self.WaitForText()
                    if self.__userQuit:
                        return 0

                    #Plays game while timer is more than 0
                    self.__raceScene = RaceScene(self.__window, self.__resolution, self.__textToWrite, self.socket)
                    self.PlayGame()
                    if self.__userQuit:
                        return 0

                    self.WaitForMatchResult()

                    #Goes to post game screen
                    self.__postGameScreen = PostGame(self.__window, self.__resolution, self.__results, self.__margin, self.__ELodiff, self.socket)
                    self.PostGame()
                    if self.__userQuit:
                        return 0

            elif userChoice == "Statistics":
                #!TEMPORARY
                pass
            elif userChoice == "Settings":
                #!TEMPORARY
                pass

    def ConnectToServer(self):
        #Before client has connected to the server
        self.__connectionScreen = ConnectionScreen(self.__window, self.__resolution)
        while self.socket is None:
            if self.__connectionScreen.socket is not None:
                self.socket = self.__connectionScreen.socket
                #Starts the client checking and sending messages
                self.__socketHandleThread = threading.Thread(target=self.__ClientHandler, daemon=True)
                self.__socketHandleThread.start()
            else:
                self.__connectionScreen.main()
                if self.__connectionScreen.userQuit:
                    self.__userQuit = True
                    return 0
                pygame.display.update()

    def Login(self):
        #Before user has logged in
        self.__loginScreen = LoginScreen(self.__window, self.__resolution, self.socket)
        while not self.__loggedIn:
            if self.__loginScreen.loggedIn:
                self.__loggedIn = True
            else:
                self.__loginScreen.main()
                if self.__loginScreen.userQuit:
                    self.__userQuit = True
                    return 0
                pygame.display.update()

    def GetChoiceFromUser(self):
        #Waits for choice from user
        while self.__mainMenu.userChoice is None:
            self.__mainMenu.main()
            if self.__mainMenu.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def WaitForGame(self):
        self.socket.msgsToSend.append("!QUEUE")
        #Wait until game is found or user cancels game being found
        #While no game is found and user hasn't quit the queue
        while not self.__matchmakingScreen.gameFound and not self.__matchmakingScreen.userClickedBackButton:
            self.__matchmakingScreen.main()
            if self.__matchmakingScreen.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def PreGameTimer(self):
        #Waits for server to start the timer
        while not self.__timerStarted:
            self.CheckMessages()
        while not self.__timerScene.timerFinished:
            self.__timerScene.main()
            if self.__timerScene.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def WaitForText(self):
        while self.__textToWrite is None:
            self.CheckMessages()

    def PlayGame(self):
        while not self.__raceScene.gameOver:
            self.__raceScene.main()
            if self.__raceScene.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def WaitForMatchResult(self):
        while self.__results is None or self.__margin is None or self.__ELodiff is None:
            self.CheckMessages()
            print(f"results = {self.__results}")
            print(f"margin = {self.__margin}")
            print(f"ELodiff = {self.__ELodiff}")

    def PostGame(self):
        #!Temp
        gothere = False
        while not self.__postGameScreen.menuButtonPressed:
            self.__postGameScreen.main()
            if not gothere:
                print("Gothere")
                gothere = True
            if self.__postGameScreen.userQuit:
                self.__userQuit= True
                return 0
            pygame.display.update()

    def CheckMessages(self):
        i = 0
        while i < len(self.socket.receivedMsgs):
            #!Temporary
            print(f"Message being checked: {self.socket.receivedMsgs[i]}")
            #If new phase started
            if self.socket.receivedMsgs[i][:11] == "!STARTTIMER":
                self.__timerStarted = True
                self.socket.receivedMsgs.pop(i)
            elif self.socket.receivedMsgs[i][:13] == "!TEXTTOWRITE:":
                self.__textToWrite = self.socket.receivedMsgs[i][13:]
                self.socket.receivedMsgs.pop(i)
            elif self.socket.receivedMsgs[i][:14] == "!MATCHOUTCOME:":
                self.__results = self.socket.receivedMsgs[i][14:]
                print(f"socketmessage = {self.socket.receivedMsgs[i][14:]}")
                if self.socket.receivedMsgs[i][14:] == "DRAW":
                    self.__margin = 0
                    self.__ELodiff = 0
                self.socket.receivedMsgs.pop(i)
            elif self.socket.receivedMsgs[i][:5] == "!ELO:":
                self.__ELodiff = self.socket.receivedMsgs[i][5:]
                self.socket.receivedMsgs.pop(i)
            elif self.socket.receivedMsgs[i][:8] == "!MARGIN:":
                self.__margin = self.socket.receivedMsgs[i][8:]
                self.socket.receivedMsgs.pop(i)
            else:
                i += 1

    #Handles getting and sending of messages
    #Necessary as if there are 2 threads then they will mistime the blocking settings
    def __ClientHandler(self):
        while self.socket.connected:
            self.socket.GetMsgs()
            self.socket.SendMsgs()