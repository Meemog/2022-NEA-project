import pygame, threading
from ClientSocket import ClientSocket
from InputHandler import InputHandler
from Boxes import InputBox
from Button import Button
from Text import Text

class Scene:
    def __init__(self, window, resolution, socket = None) -> None:
        self.userQuit = False
        self.socket = socket

        #Whether or not these are held down
        self._shift = False
        self._alt = False
        self._ctrl = False
        self._backspace = False

        self._timeSinceLastBackspace = 0

        #Used to redner things on screen
        self._listOfBoxObjects = []
        self._listOfButtonObjects = []
        self._listOfTextObjects = []

        self._window = window
        self._resolution = resolution

        self._clock = pygame.time.Clock()
        self._inputHandler = InputHandler()

    def main(self):
        self._clock.tick()
        self._timeSinceLastBackspace += self._clock.get_time()

        self.HandleInputs()
        self.Render()

    def Render(self):
        for box in self._listOfBoxObjects:
            box.Render(self._window)
        for button in self._listOfButtonObjects:
            button.Render(self._window)
        for textObject in self._listOfTextObjects:
            textObject.Render(self._window)

    def HandleInputs(self):
        self._inputHandler.CheckInputs()
        while self._inputHandler.inputsPriorityQueue.GetLength() != 0:
            input = self._inputHandler.inputsPriorityQueue.Dequeue()
            
            if input[1] == "QUIT":
                self.userQuit = True

            elif input[1] == "SHIFTDOWN":
                self._shift = True
            elif input[1] == "SHIFTUP":
                self._shift = False
            elif input[1] == "ALTDOWN":
                self._alt = True
            elif input[1] == "ALTUP":
                self._alt = False
            elif input[1] == "CONTROLDOWN":
                self._ctrl = True
            elif input[1] == "CONTROLUP":
                self._ctrl = False
            elif input[1] == "BACKSPACEDOWN":
                self._backspace = True
                self._timeSinceLastBackspace = -200
            elif input[1] == "BACKSPACEUP":
                self._backspace = False

#Displays text that changes in the middle of the screen
class ConnectionScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.connected = False

        #Used for changing the number of dots in the text
        self._timeSinceLastMessageUpdate = 0
        self._numberOfDots = 0

        #Setting up text
        self._font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))
        self.__textObject = Text(self._font, text = "Connecting to server")
        location = ((self._resolution[0] - self.__textObject.textRender.get_size()[0]) / 2, self._resolution[1] / 2)
        self.__textObject.location = location

        self._listOfTextObjects = [self.__textObject]
        
        #Used for connecting to server
        self._serverSearchThread = threading.Thread(target=self.ConnectToServer, daemon=True)
        self._serverSearchThread.start()

    def main(self):
        super().main()
        self._timeSinceLastMessageUpdate += self._clock.get_time()
        if self._timeSinceLastMessageUpdate >= 700:
            self.__textObject.SetText("Connecting to server" + "." * self._numberOfDots)
            self._numberOfDots += 1
            self._timeSinceLastMessageUpdate = 0

    def ConnectToServer(self):
        self.socket = ClientSocket()
        self.connected = True