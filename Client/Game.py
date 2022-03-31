import pygame, threading
from Scene import ConnectionScreen

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
        self.resolutionScale = (self.resolution[0] / 1920, self.resolution[1] / 1080)

        #Various scenes get defined here
        self.connectionScreen = ConnectionScreen(self.window, self.resolution, self.resolutionScale)

        self.scenes = [self.connectionScreen]
        self.activeScene = self.connectionScreen
        
    def main(self):
        while not self.userQuit:
            if self.socket is None:
                self.activeScene = self.connectionScreen
            # else:
            #     if not self.loginScreen.loggedIn:
            #         self.activeScene = self.loginScreen
            #     elif not self.mainMenu.userHasMadeChoice:
            #         self.activeScene = self.mainMenu
            #     elif not self.matchmakingScreen.gameFound:
            #         self.activeScene = self.matchmakingScreen
            
            self.activeScene.main()
            if self.activeScene.userQuit:
                self.userQuit = True

            if self.socket is None and self.connectionScreen.connected:
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