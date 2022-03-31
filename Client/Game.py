import pygame, threading
from Scene import ConnectionScreen, LoginScreen

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

        self.__scenes = [self.__connectionScreen]
        self.__activeScene = self.__connectionScreen
        
    def main(self):
        while not self.__userQuit:
            if self.socket is None:
                self.__activeScene = self.__connectionScreen
            else:
                if not self.__loginScreen.loggedIn:
                    self.__activeScene = self.__loginScreen
            #     elif not self.mainMenu.userHasMadeChoice:
            #         self.__activeScene = self.mainMenu
            #     elif not self.matchmakingScreen.gameFound:
            #         self.__activeScene = self.matchmakingScreen
            
            self.__activeScene.main()
            if self.__activeScene.userQuit:
                self.__userQuit = True

            if self.socket is None and self.__connectionScreen.connected:
                self.socket = self.__connectionScreen.socket
        
                #Starts the client checking and sending messages
                self.__msgGetThread = threading.Thread(target = self.socket.GetMsgs, daemon = True)
                self.__msgSendThread = threading.Thread(target = self.socket.SendMsgs, daemon = True)
                self.__msgGetThread.start()
                self.__msgSendThread.start()
                
                #Applies new socket to all scenes, by default they are None
                for scene in self.__scenes:
                    scene.socket = self.__connectionScreen.socket

            pygame.display.update()
            
        if self.socket is not None:
            self.socket.EndConnection()