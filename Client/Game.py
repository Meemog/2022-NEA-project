import pygame
import threading
from TextBox import TextBox
from Renderer import Renderer
from ClientSocket import ClientSocket
from LoginScreen import LoginScreen
from MainMenu import MainMenu

class Game:
    def __init__(self, dispWidth, dispHeight):
        self.ConnectToServer()
        self.connected = True

        if not self.userQuit:
            self.__loginScreen = LoginScreen((dispWidth, dispHeight), self.clientSocket)
            self.__mainMenu = MainMenu((dispWidth, dispHeight))

            font = pygame.font.SysFont("Courier New", int(dispHeight*42/1080))  #sets font to Courier New (font with constant letter size)
            self.__textBox = TextBox(int(self.__dispWidth - (self.__dispWidth * 2/5)), int(50 * self.__dispHeight / 1080), (int(self.__dispWidth / 5), int(6 * self.__dispHeight / 20)), (40,40,40), (30,30,30), (255,144,8), font, (160,160,160))

            #A thread that will get messages and send messages to the server
            self.__SocketHandleThread = threading.Thread(target=self.__HandleSocket, daemon=True)
            self.__SocketHandleThread.start()

    def main(self, window):
            #Queues into matchmaking
            self.clientSocket.msgsToSend.append("!QUEUE")

            timeSinceLastTimerUpdate = 0

            #Main loop starts here
            while self.__gameTimer >= 0 and not self.userQuit:
                #Draws the background and empty textbox
                self.__renderer.Render(self.__window, self.__textBox)
                self.__gameClock.tick()

                #Handles userinput
                self.__HandleInput()
                self.__CheckForBackspace()
                self.__timeSinceLastBackspace += self.__gameClock.get_time()
                
                #Handles messages from server
                self.__HandleMessages()

                if self.__backText == " ":
                    #If game has not started
                    if self.timerActive:
                        #Display seconds left until start and removes time since last frame from timer
                        self.__renderer.RenderTimer(self.__window, (self.__dispWidth, self.__dispHeight), self.__timerUntilGameStart)
                        self.__timeSinceLastCountdown += self.__gameClock.get_time()
                        
                        if self.__timeSinceLastCountdown >= 1000:
                            self.__timerUntilGameStart -= 1
                            self.__timeSinceLastCountdown -= 1000

                        if self.__timerUntilGameStart <= 0:
                            self.timerActive = False
                    else:
                        self.__renderer.RenderWaitingText(self.__window, (self.__dispWidth, self.__dispHeight))

                #When game has started
                elif self.__gameTimer >= 0:
                    self.__renderer.RenderTimer(self.__window, (self.__dispWidth, self.__dispHeight), self.__gameTimer)
                    timeSinceLastTimerUpdate += self.__gameClock.get_time()
                    #Every second displays the current time left
                    if timeSinceLastTimerUpdate >= 1000:
                        self.__gameTimer -= 1
                        timeSinceLastTimerUpdate -= 1000

                pygame.display.update()
            self.clientSocket.EndConnection()
    
    def ConnectToServer(self):
        #Attempts to connect to the server, will continue indefinitely until a server is found
        self.__serverFound = False
        self.__serverSearchThread = threading.Thread(target=self.__SearchForServer)
        self.__serverSearchThread.start()
        while not self.__serverFound and not self.userQuit:
            self.__CheckIfUserQuit()

    #Tries to connect to server, used in init to allow instant quitting when user alt+f4
    #This runs in another thread
    def __SearchForServer(self):
        while not self.__serverFound and not self.userQuit:
            try:
                self.clientSocket = ClientSocket()
                self.__serverFound = True
            except:
                print("Failed to connect to server, trying again")

    def __HandleMessages(self):
        pass

    def __HandleSocket(self):
        while self.clientSocket.connected or self.clientSocket.msgsToSend != []:
            self.clientSocket.SendMsgs()
            self.clientSocket.GetMsgs()