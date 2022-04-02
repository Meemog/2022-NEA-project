import pygame, threading
from Scene import ConnectionScreen, LoginScreen, MainMenu, MatchmakingScreen, TimerScene

class Game:
    def __init__(self, window):
        self.socket = None
        self.__window = window
        self.__userQuit = False

        #Temporary variable which will be set once the socket is connected
        self.__socketHandleThread = None

        self.__resolution = pygame.display.Info()
        self.__resolution = (self.__resolution.current_w / 1920, self.__resolution.current_h / 1080)

        #Various scenes get defined here
        self.__connectionScreen = ConnectionScreen(self.__window, self.__resolution)
        self.__loginScreen = LoginScreen(self.__window, self.__resolution)
        self.__mainMenu = MainMenu(self.__window, self.__resolution)
        self.__matchmakingScreen = MatchmakingScreen(self.__window, self.__resolution)
        self.__timerScene = TimerScene(self.__window, self.__resolution)

        self.__scenes = [self.__connectionScreen, self.__loginScreen, self.__mainMenu, self.__matchmakingScreen, self.__timerScene]
        self.__activeScene = self.__connectionScreen
        
    def main(self):
        while not self.__userQuit:
            #Checking what scene should be active
            if self.socket is None:
                if self.__connectionScreen.socket is not None:
                    self.socket = self.__connectionScreen.socket
                    #Starts the client checking and sending messages
                    self.__socketHandleThread = threading.Thread(target=self.ClientHandler, daemon=True)
                    self.__socketHandleThread.start()

                    for scene in self.__scenes:
                        scene.socket = self.__connectionScreen.socket
                else:
                    self.__activeScene = self.__connectionScreen
            #Checking what scene should be active after connected to server
            else:
                #Sends user to login screen if they are not logged in
                if not self.__loginScreen.loggedIn:
                    self.__activeScene = self.__loginScreen
                #Sends user to main menu if they have not made a choice
                elif self.__mainMenu.userChoice is None:
                    self.__activeScene = self.__mainMenu
                #Checks for users choice if it isn't None
                elif self.__activeScene == self.__mainMenu and self.__mainMenu.userChoice is not None:
                    #User choice cannot be quit by this point as that is checked directly after the main() of main menu
                    if self.__mainMenu.userChoice == "Play":
                        self.__matchmakingScreen.Reset()
                        self.__activeScene = self.__matchmakingScreen
                        self.socket.msgsToSend.append("!QUEUE")
                    elif self.__mainMenu.userChoice == "Statistics":
                        pass
                    elif self.__mainMenu.userChoice == "Settings":
                        pass

                #Checks message if socket isn't none
                self.CheckMessages()

            #Dequeues from matchmaking if user presses return button
            if self.__activeScene == self.__matchmakingScreen and self.__matchmakingScreen.userClickedBackButton:
                self.socket.msgsToSend.append("!DEQUEUE")
                self.__mainMenu.Reset()
                self.__activeScene = self.__mainMenu

            self.__activeScene.main()
            if self.__activeScene.userQuit:
                self.__userQuit = True

            pygame.display.update()
            
        if self.socket is not None:
            self.socket.EndConnection()

    def CheckMessages(self):
        i = 0
        while i < len(self.socket.receivedMsgs):
            #If new phase started
            if self.socket.receivedMsgs[i][:7] == "!STAGE:":
                print(f"Check message: {self.socket.receivedMsgs[i]}")
                stage = self.socket.receivedMsgs[i][7:]
                if stage == "TIMER":
                    self.__activeScene = self.__timerScene
                #Removes this message from list of messages
                self.socket.receivedMsgs.pop(i)
            else:
                i += 1

    #Handles getting and sending of messages
    #Necessary as if there are 2 threads then they will mistime the blocking settings
    def ClientHandler(self):
        while self.socket.connected:
            self.socket.GetMsgs()
            self.socket.SendMsgs()