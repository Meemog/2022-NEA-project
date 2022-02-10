import pygame
import threading
from TextBox import TextBox
from Renderer import Renderer
from ClientSocket import ClientSocket
from LoginScreen import LoginScreen
from MainMenu import MainMenu

class Game:
    def __init__(self, dispWidth, dispHeight):
        self.__gameClock = pygame.time.Clock()  #Makes a clock object
        self.__timeBetweenBacspaces = 50        #Delay between backspaces when backspace is held down
        self.__timeSinceLastBackspace = 0     
        self.__deleting = False    
        self.__ctrl = False                     #Boolean that is true for the duration of the backspace key being held down
        self.__renderer = Renderer(dispHeight)            #Creates Renderer object
        self.__backText = " "
        self.connected = True
        self.userQuit = False 
        self.__timerUntilGameStart = 0
        self.__gameTimer = 30
        self.__timeSinceLastCountdown = 0
        self.__dispWidth = dispWidth
        self.__dispHeight = dispHeight
        self.__settings = {"Volume": 50, "Res": (dispWidth, dispHeight)}
        
        self.ConnectToServer()
        self.__loginScreen = LoginScreen((dispWidth, dispHeight), self.clientSocket)
        self.__mainMenu = MainMenu((dispWidth, dispHeight))

        font = pygame.font.SysFont("Courier New", int(dispHeight*42/1080))  #sets font to Courier New (font with constant letter size)
        self.__textBox = TextBox(int(self.__dispWidth - (self.__dispWidth * 2/5)), int(50 * self.__dispHeight / 1080), (int(self.__dispWidth / 5), int(6 * self.__dispHeight / 20)), (40,40,40), (30,30,30), (255,144,8), font, (160,160,160))

        #A thread that will get messages and send messages to the server
        self.__SocketHandleThread = threading.Thread(target=self.__HandleSocket, daemon=True)
        self.__SocketHandleThread.start()

    def main(self, window):
        self.__window = window
        #Ends program if no server was found before player quit
        if not self.__serverFound:
            return "Player quit while looking for server"
        else: 
            self.clientSocket.msgsToSend.append("[Connection established with client]")
            print("Connected to server")

        while not self.userQuit:
            if not self.__loginScreen.main(self.__window):
                self.clientSocket.EndConnection()
                return "Player quit while logging in"

            if not self.__mainMenu.Run(self.__window):
                self.clientSocket.EndConnection()
                return "Player quit in menu"

            self.timerActive = False

            #Queues into matchmaking
            self.clientSocket.msgsToSend.append("!QUEUE")

            timeSinceLastTimerUpdate = 0

            #Main loop starts here
            while self.__gameTimer >= 0:
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

    def __HandleMessages(self):
        while self.clientSocket.receivedMsgs != []:
            if self.clientSocket.receivedMsgs[0] == "!DISCONNECT":
                self.clientSocket.connected = False
            
            elif self.clientSocket.receivedMsgs[0][:10] == "!BACKTEXT:":
                self.__backText = self.clientSocket.receivedMsgs[0][10:]
                #Creates a textbox object and passes arguments through it // refer to TextBox.py
                self.__textBox.SetPreviewText(self.__backText)
                self.timerActive = False

            elif self.clientSocket.receivedMsgs[0][:23] == "!SECONDSLEFTUNTILSTART:":
                self.timerActive = True
                self.__timerUntilGameStart = int(self.clientSocket.receivedMsgs[0][23:]) - 2

            self.clientSocket.receivedMsgs.pop(0)

    #Tries to connect to server, used in init to allow instant quitting when user alt+f4
    #This runs in another thread
    def __SearchForServer(self):
        while not self.__serverFound and not self.userQuit:
            try:
                self.clientSocket = ClientSocket()
                self.__serverFound = True
            except:
                print("Failed to connect to server, trying again")

    #Returns true if the player tries to quit the game
    #Used in the init for Client to allow player to quit while it is searching for a server
    def __CheckIfUserQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.userQuit = True

    #Used to translate player input into actions on screen, such as typing a letter or deleting a letter
    def __HandleInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:           #If alt + f4 pressed or quit button (in the future)
                self.userQuit = True

            elif event.type == pygame.MOUSEBUTTONDOWN:  #When mouse is clicked
                clickLocation = pygame.mouse.get_pos()  
                if self.__textBox.box.collidepoint(clickLocation):
                    self.__textBox.SetActive()  #Sets textbox to be active if it was clicked on 
                
                else:
                    self.__textBox.SetDormant() #Sets textbox to be dormant if anywhere else clicked

            elif event.type == pygame.KEYDOWN:  #When button is pressed
                if event.key == pygame.K_BACKSPACE: #When backspace pressed
                    self.__deleting = True

                    if self.__textBox.isActive:
                        self.__textBox.DeleteLetter(self.__ctrl)    #Deletes letter
                        self.__timeSinceLastBackspace = -200    #Causes delay until letters are deleted automatically
                
                elif event.key == pygame.K_RETURN:
                    pass

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:   #Used for deleting entire letters
                    self.__ctrl = True
                
                else:
                    if self.__textBox.isActive:
                        self.__textBox.AddLetter(event.unicode) #Adds letter to textbox if anything else is pressed
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.__deleting = False
                
                elif event.key == pygame.K_RETURN:
                    pass

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.__ctrl = False

    def __CheckForBackspace(self):
        #Deletes text while backspace being held down
        if self.__deleting and self.__timeSinceLastBackspace > self.__timeBetweenBacspaces and self.__inputHandler.typing:
            self.__textBox.DeleteLetter(self.__ctrl)
            self.__timeSinceLastBackspace = 0

    def __HandleSocket(self):
        while self.clientSocket.connected or self.clientSocket.msgsToSend != []:
            self.clientSocket.SendMsgs()
            self.clientSocket.GetMsgs()