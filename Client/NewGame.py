import pygame, threading
from Scene import ConnectingToServer, LoginScreen, MainMenu, MatchmakingScreen

class Game:
    def __init__(self, window):
        self.window = window
        self.connected = False
        self.userQuit = False
        self.socket = None
        self.msgSendThread = None
        self.msgGetThread = None

        self.resolution = pygame.display.Info()
        self.resolution = (self.resolution.current_w, self.resolution.current_h)

        #Various scenes get defined here
        self.connectionScreen = ConnectingToServer(self.window, self. resolution, None)
        self.loginScreen = LoginScreen(self.window, self.resolution, None)
        self.mainMenu = MainMenu(self.window, self.resolution, None)
        self.matchmakingScreen = MatchmakingScreen(self.window, self.resolution, None)

        self.scenes = [self.connectionScreen, self.loginScreen, self.mainMenu, self.matchmakingScreen]
        self.activeScene = self.connectionScreen
        
    def main(self):
        while not self.userQuit:
            if self.socket is None:
                self.activeScene = self.connectionScreen
            else:
                if not self.loginScreen.loggedIn:
                    self.activeScene = self.loginScreen
                elif not self.mainMenu.userHasMadeChoice:
                    self.activeScene = self.mainMenu
                elif not self.matchmakingScreen.gameFound:
                    self.activeScene = self.matchmakingScreen
            
            self.activeScene.main()
            if self.activeScene.userQuit:
                self.userQuit = True

            if self.activeScene == self.connectionScreen and self.socket is None:
                self.socket = self.connectionScreen.socket
        
                #Starts the client checking and sending messages
                self.msgGetThread = threading.Thread(target = self.socket.GetMsgs, daemon = True)
                self.msgSendThread = threading.Thread(target = self.socket.SendMsgs, daemon = True)
                self.msgGetThread.start()
                self.msgSendThread.start()
                
                #Applies new socket to all scenes, by default they are None
                for scene in self.scenes:
                    scene.socket = self.connectionScreen.socket

            pygame.display.update()