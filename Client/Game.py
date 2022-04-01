import pygame, threading
from Scene import ConnectionScreen, LoginScreen, MainMenu, MatchmakingScreen

class Game:
    def __init__(self, window):
        self.socket = None
        self.__window = window
        self.__connected = False
        self.__userQuit = False
        self.__msgSendThread = None
        self.__msgGetThread = None

        self.__resolution = pygame.display.Info()
        self.__resolution = (self.__resolution.current_w / 1920, self.__resolution.current_h / 1080)

        #Various scenes get defined here
        self.__connectionScreen = ConnectionScreen(self.__window, self.__resolution)
        self.__loginScreen = LoginScreen(self.__window, self.__resolution)
        self.__mainMenu = MainMenu(self.__window, self.__resolution)
        self.__matchmakingScreen = MatchmakingScreen(self.__window, self.__resolution)

        self.__scenes = [self.__connectionScreen, self.__loginScreen, self.__mainMenu]
        self.__activeScene = self.__connectionScreen
        
    def main(self):
        while not self.__userQuit:
            if self.socket is None:
                if self.__connectionScreen.socket is not None:
                    self.socket = self.__connectionScreen.socket
                    #Starts the client checking and sending messages
                    self.__msgGetThread = threading.Thread(target = self.socket.GetMsgs, daemon = True)
                    self.__msgSendThread = threading.Thread(target = self.socket.SendMsgs, daemon = True)
                    self.__msgGetThread.start()
                    self.__msgSendThread.start()
                
                    for scene in self.__scenes:
                        scene.socket = self.__connectionScreen.socket
                else:
                    self.__activeScene = self.__connectionScreen
            else:
                if not self.__loginScreen.loggedIn:
                    self.__activeScene = self.__loginScreen
                elif self.__mainMenu.userChoice is None:
                    self.__activeScene = self.__mainMenu
                elif self.__mainMenu.userChoice is not None and self.__activeScene == self.__mainMenu:
                    #User choice cannot be quit by this point as that is checked directly after the main() of main menu
                    if self.__mainMenu.userChoice == "Play":
                        self.__activeScene = self.__matchmakingScreen
                        self.socket.msgsToSend.append("!QUEUE")
                    elif self.__mainMenu.userChoice == "Statistics":
                        pass
                    elif self.__mainMenu.userChoice == "Settings":
                        pass

            self.__activeScene.main()
            if self.__activeScene.userQuit:
                self.__userQuit = True

            pygame.display.update()
            
        if self.socket is not None:
            self.socket.EndConnection()