import pygame, threading, pickle
from Scene import *

class Game:
    def __init__(self, window, settings):
        self.socket = None
        self.settings = settings
        self.__loggedIn = False
        self.__window = window
        self.__userQuit = False

        #Temporary variable which will be set once the socket is connected
        self.__socketHandleThread = None

        self.__resolution = pygame.display.Info()
        self.__resolution = (self.__resolution.current_w / 1920, self.__resolution.current_h / 1080)

        self.__connectionScreen : ConnectionScreen = None
        self.__loginScreen : LoginScreen = None
        self.__registerScreen : RegisterScreen = None
        self.__mainMenu : MainMenu = None
        self.__settingsScreen : SettingsScreen = None
        self.__statisticsScreen : StatisticsScreen = None
        self.__matchmakingScreen : MatchmakingScreen = None
        self.__timerScene : TimerScene = None
        self.__raceScene : RaceScene = None
        self.__postGameScreen : PostGame = None

        self.__timerStarted = False
        self.__textToWrite = None
        self.__results = None

    def main(self):
        #Connects to server
        self.__ConnectToServer()
        #I couldn't come up with a more readable solution for having to end the game after any of these scenes than to simply check after every one
        #I previously had a solution with an activescene attribute but that was unreadable and provided no real benefit
        if self.__userQuit:
            return 0

        while not self.__loggedIn:
            #Goes to loginscreen
            self.__Login()
            if self.__userQuit:
                return 0
            elif self.__loginScreen.userWantsToCreateAccount:
                self.__Register()
                if self.__userQuit:
                    return 0
                if self.__registerScreen.registered:
                    self.__loggedIn = True

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
            self.__stats = None

            #Goes to main menu to get choice from user
            self.__GetChoiceFromUser()
            if self.__userQuit:
                return 0
            userChoice = self.__mainMenu.userChoice

            if userChoice == "Play":
                #Goes to matchmaking screen
                self.__WaitForGame()
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
                    self.__PreGameTimer()
                    if self.__userQuit:
                        return 0
                    #Waits for previewtext from server
                    self.__WaitForText()
                    if self.__userQuit:
                        return 0

                    #Plays game while timer is more than 0
                    self.__raceScene = RaceScene(self.__window, self.__resolution, self.__textToWrite, self.socket)
                    self.__PlayGame()
                    if self.__userQuit:
                        return 0

                    self.__WaitForMatchResult()

                    #Goes to post game screen
                    self.__postGameScreen = PostGame(self.__window, self.__resolution, self.__results, self.__margin, self.__ELodiff, self.socket)
                    self.__PostGame()
                    if self.__userQuit:
                        return 0

            elif userChoice == "Statistics":
                self.__WaitForData()
                self.__ShowStatistics()

            elif userChoice == "__Settings":
                self.__Settings()
                if self.__userQuit:
                    return 0

    def __ConnectToServer(self):
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

    def __Login(self):
        #Before user has logged in
        self.__loginScreen = LoginScreen(self.__window, self.__resolution, self.socket)
        while not self.__loggedIn and not self.__loginScreen.userWantsToCreateAccount:
            if self.__loginScreen.loggedIn:
                self.__loggedIn = True
            else:
                self.__loginScreen.main()
                if self.__loginScreen.userQuit:
                    self.__userQuit = True
                    return 0
                pygame.display.update()

    def __Register(self):
        #When user wants to create account
        self.__registerScreen = RegisterScreen(self.__window, self.__resolution, self.socket)
        while not self.__registerScreen.backbuttonPressed and not self.__registerScreen.registered:
            self.__registerScreen.main()
            if self.__registerScreen.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __GetChoiceFromUser(self):
        #Waits for choice from user
        while self.__mainMenu.userChoice is None:
            self.__mainMenu.main()
            if self.__mainMenu.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __WaitForGame(self):
        self.socket.msgsToSend.append("!QUEUE")
        #Wait until game is found or user cancels game being found
        #While no game is found and user hasn't quit the queue
        while not self.__matchmakingScreen.gameFound and not self.__matchmakingScreen.userClickedBackButton:
            self.__matchmakingScreen.main()
            if self.__matchmakingScreen.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __PreGameTimer(self):
        #Waits for server to start the timer
        while not self.__timerStarted:
            self.__CheckMessages()
        while not self.__timerScene.timerFinished:
            self.__timerScene.main()
            if self.__timerScene.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __WaitForText(self):
        while self.__textToWrite is None:
            self.__CheckMessages()

    def __Settings(self):
        self.__settingsScreen = SettingsScreen(self.__window, self.__resolution, self.settings, self.socket)
        while not self.__settingsScreen.backButtonPressed:
            self.__settingsScreen.main()
            if self.__settingsScreen.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __WaitForData(self):
        self.socket.msgsToSend.append("!STATISTICS")
        while self.__stats is None:
            self.__CheckMessages()

    def __ShowStatistics(self):
        self.__statisticsScreen = StatisticsScreen(self.__window, self.__resolution, self.__stats, self.socket)
        while not self.__statisticsScreen.backButtonPressed:
            self.__statisticsScreen.main()
            if self.__statisticsScreen.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __PlayGame(self):
        while not self.__raceScene.gameOver:
            self.__raceScene.main()
            if self.__raceScene.userQuit:
                self.__userQuit = True
                return 0
            pygame.display.update()

    def __WaitForMatchResult(self):
        while self.__results is None or self.__margin is None or self.__ELodiff is None:
            self.__CheckMessages()

    def __PostGame(self):
        while not self.__postGameScreen.menuButtonPressed:
            self.__postGameScreen.main()
            if self.__postGameScreen.userQuit:
                self.__userQuit= True
                return 0
            pygame.display.update()

    def __CheckMessages(self):
        i = 0
        while i < len(self.socket.receivedMsgs):
            #If new phase started
            try: 
                self.__stats = pickle.loads(self.socket.receivedMsgs[i])
                print("Pickle acquired")
                self.socket.receivedMsgs.pop(i)
            except:
                if self.socket.receivedMsgs[i][:11] == "!STARTTIMER":
                    self.__timerStarted = True
                    self.socket.receivedMsgs.pop(i)
                elif self.socket.receivedMsgs[i][:13] == "!TEXTTOWRITE:":
                    self.__textToWrite = self.socket.receivedMsgs[i][13:]
                    self.socket.receivedMsgs.pop(i)
                elif self.socket.receivedMsgs[i][:14] == "!MATCHOUTCOME:":
                    self.__results = self.socket.receivedMsgs[i][14:]
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