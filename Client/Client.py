import pygame
import threading
from TextBox import TextBox
from InputHandler import InputHandler
from Renderer import Renderer
from Backend.client import ClientSocket

class Client:
    def __init__(self):
        self.__gameClock = pygame.time.Clock()  #Makes a clock object
        self.__inputHandler = InputHandler()    #Creates an InputHandler object
        self.__timeBetweenBacspaces = 50        #Delay between backspaces when backspace is held down
        self.__timeSinceLastBackspace = 0     
        self.__deleting = False    
        self.__ctrl = False             #Boolean that is true for the duration of the backspace key being held down
        self.__renderer = Renderer()            #Creates Renderer object
        self.__backText = " "
        self.__GAMELOOP = False

        #Attempts to connect to the server, will continue indefinitely until a server is found
        self.__serverFound = False
        serverSearchThread = threading.Thread(target=self.__SearchForServer(), args=self)
        serverSearchThread.start()
        while not self.__serverFound:
            if self.__CheckIfUserQuit():
                break

    def main(self, window,  dispWidth, dispHeight):
        #Ends program if no server was found before player quit
        if not self.__serverFound:
            return "Player quit while looking for server"
        #Waits for game to start
        waiting = True
        self.__clientSocket.SendMsg("ConnectionEstablished")
        while waiting:  
            if self.__CheckIfUserQuit():
                self.__clientSocket.SendMsg("!DISCONNECT")
                return "Player quit while matchmaking"

            self.__backText = self.__GetBackText()
            if self.__backText != " ":
                #Creates a textbox object and passes arguments through it // refer to TextBox.py
                self.__textBox = TextBox(int(dispWidth - (dispWidth * 2/5)), int(50 * dispHeight / 1080), (int(dispWidth / 5), int(6 * dispHeight / 20)), (40,40,40), (30,30,30), (255,144,8), int(dispHeight*42/1080), self.__backText, (160,160,160), "Comic Sans MS")
                waiting = False
                self.__GAMELOOP = True
                waiting = False
            #Checks for player closing the application
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__clientSocket.EndConnection()
                    waiting = False

        #Happens after game has started
        while self.__GAMELOOP:
            self.__gameClock.tick()                  
            pygame.time.delay(30)                       #Determines max fps of game
            commands = self.__inputHandler.HandleInput(self.__textBox.box) #Gets list of input events
            self.TranslateInput(commands)   #Converts keyboard inputs into changes in attributes    
            self.__CheckForBackspace()        #Function for checking if backspace is held down
                        
            self.__timeSinceLastBackspace += self.__gameClock.get_time()    #Adds time since last frame to time since last backspace
            self.__renderer.Render(window, self.__textBox)  #Draws everything
        return 0

    #Tries to connect to server, used in init to allow instant quitting when user alt+f4
    #This runs in another thread
    def __SearchForServer(self):
        while not self.__serverFound:
            try:
                self.__clientSocket = ClientSocket()
                self.__serverFound = True
            except:
                print("Failed to connect to server, trying again")

    #Returns true if the player tries to quit the game
    #Used in the init for Client to allow player to quit while it is searching for a server
    def __CheckIfUserQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def TranslateInput(self, commands):
        for command in commands:
            if command == "QUIT":                   #If alt + f4 pressed or quit button (in the future)
                self.__GAMELOOP = False

            elif command[0] == "K":                 #K is always followed by another letter (letter that was pressed)
                command = command[1:]               #Removes K
                self.__textBox.AddLetter(command)   #Adds letter to textbox

            elif command == "CLICKED ON BOX":       
                self.__textBox.SetActive()          #Changes colour and enables typing in the textbox

            elif command == "CLICKED OUT OF BOX":   #Changes colour and disables typing in the textbox
                self.__textBox.SetDormant()

            elif command == "BACKSPACE DOWN":       
                self.__textBox.DeleteLetter(self.__ctrl)       #Removes letter form textbox
                self.__deleting = True              #True until BACKSPACE UP
                self.__timeSinceLastBackspace = -200    #Gives 0.2 second delay until deleting starts

            elif command == "BACKSPACE UP":
                self.__deleting = False

            elif command == "CONTROL DOWN":
                self.__ctrl = True
            
            elif command == "CONTROL UP":
                self.__ctrl = False

    def __CheckForBackspace(self):
        #Deletes text while backspace being held down
        if self.__deleting and self.__timeSinceLastBackspace > self.__timeBetweenBacspaces and self.__inputHandler.typing:
            self.__textBox.DeleteLetter(self.__ctrl)
            self.__timeSinceLastBackspace = 0

    #Gets text that should be used in the background
    def __GetBackText(self):
        msg = self.__clientSocket.GetMsgs()
        if msg[:9] == "BACKTEXT:":
            return msg[9:]

        else: 
            return " "
