import pygame, threading, socket
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

        for buttonObject in self._listOfButtonObjects:
            if buttonObject.CheckForCollision(pygame.mouse.get_pos()):
                buttonObject.SetActive()
            else:
                buttonObject.SetInactive()

        self.Render()

    def Render(self):
        self._window.fill((0,0,0))
        for box in self._listOfBoxObjects:
            box.Render(self._window)
        for button in self._listOfButtonObjects:
            button.Render(self._window)
        for textObject in self._listOfTextObjects:
            textObject.Render(self._window)

    def HandleInputs(self):
        self._inputHandler.CheckInputs()
        unusedInputs = []
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
            else:
                unusedInputs.append(input)
        for input in unusedInputs:
            self._inputHandler.inputsPriorityQueue.Enqueue(input[0], input[1])

#Displays text that changes in the middle of the screen
class ConnectionScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.connected = False

        #Used for changing the number of dots in the text
        self._timeSinceLastMessageUpdate = 0
        self._numberOfDots = 0

        self._font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))

        textSize = self._font.size("Connecting to server...")
        textLocation = ((self._resolution[0] * 1920 - textSize[0]) / 2, (self._resolution[1] * 1080 - textSize[1]) / 2)

        self._textToRender = "Connecting to server"
        self.__textObject = Text(self._font, text=self._textToRender, location=textLocation)

        self._listOfTextObjects = [self.__textObject]
        
        #Used for connecting to server
        self._serverSearchThread = threading.Thread(target=self.ConnectToServer, daemon=True)
        self._serverSearchThread.start()

    def main(self):
        super().main()
        self._timeSinceLastMessageUpdate += self._clock.get_time()
        if self._timeSinceLastMessageUpdate >= 700:
            self._textToRender = "Connecting to server" + "." * self._numberOfDots
            self.__textObject.SetText(self._textToRender)
            self._numberOfDots += 1
            if self._numberOfDots == 4:
                self._numberOfDots = 0
            self._timeSinceLastMessageUpdate = 0

    def ConnectToServer(self):
        while not self.connected:
            try:
                self.socket = ClientSocket()
                self.connected = True
            except socket.error:
                pass

class LoginScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.loggedIn = False
        self.__detailsSent = False

        inputBoxFont = pygame.font.SysFont("Courier New", int(36 * self._resolution[1]))

        #Need 2 inputboxes, 2 text and 1 button
        inputBoxSize = (int(625 * self._resolution[0]), int(60 * self._resolution[1]))
        #Button needs to be centred and 400 pixels down
        usernameBoxLocation = ((self._resolution[0] * 1920 - inputBoxSize[0]) / 2, 400 * self._resolution[1])
        passwordBoxLocation = ((self._resolution[1] * 1920 - inputBoxSize[0]) / 2, 540 * self._resolution[1])
        usernameRect = pygame.Rect(usernameBoxLocation[0], usernameBoxLocation[1], inputBoxSize[0], inputBoxSize[1])
        passwordRect = pygame.Rect(passwordBoxLocation[0], passwordBoxLocation[1], inputBoxSize[0], inputBoxSize[1])
        self.__usernameBox = InputBox(usernameRect, inputBoxFont, self._resolution, (40,40,40), (25,25,25), (255,255,255), "")
        self.__passwordBox = InputBox(passwordRect, inputBoxFont, self._resolution, (40,40,40), (25,25,25), (255,255,255), "")

        continueButtonSize = (400 * self._resolution[0], 60 * self._resolution[1])
        #Button needs to be centred and 680 pixels down
        continueButtonLocation = ((self._resolution[0] * 1920 - continueButtonSize[0]) / 2, 680 * self._resolution[1])
        continueButtonRect = pygame.Rect(continueButtonLocation[0], continueButtonLocation[1], continueButtonSize[0], continueButtonSize[1])
        self.__continueButton = Button(continueButtonRect, (40,40,40), (25,25,25), (255,255,255), text="Continue")

        #Text needs to be 5 pixels to the right of the corresponding box and needs to be 25 pixels above (so 25 pixels and the height of the text itself)
        usernameTextSize = inputBoxFont.size("Username")
        usernameTextLocation = (usernameBoxLocation[0] + 5 * self._resolution[0], usernameBoxLocation[1] - 25 * self._resolution[1] - usernameTextSize[1])
        self.__usernameText = Text(inputBoxFont, text="Username", location=usernameTextLocation)
        passwordTextSize = inputBoxFont.size("Password")
        passwordTextLocation = (passwordBoxLocation[0] + 5 * self._resolution[0], passwordBoxLocation[1] - 25 * self._resolution[1] - passwordTextSize[1])
        self.__passwordText = Text(inputBoxFont, text="Password", location=passwordTextLocation)

        #These lists are used to render things on the screen, they are iterated through
        self._listOfBoxObjects = [self.__usernameBox, self.__passwordBox]
        self._listOfButtonObjects = [self.__continueButton]
        self._listOfTextObjects = [self.__usernameText, self.__passwordText]

    def main(self):
        super().main()
        #Automatic removal of text every 50 milliseconds
        if self._backspace and self._timeSinceLastBackspace >= 50 and not self.__continueButton.clicked:
            for box in self._listOfBoxObjects:
                if box.isActive:
                    box.RemoveLetter(self._ctrl)
        if self.__continueButton.clicked and not self.__detailsSent:
            username = self.__usernameBox.text
            password = self.__passwordBox.text
            self.socket.msgsToSend.Enqueue(f"!LOGIN:{username},{password}")
            self.__detailsSent = True

    def HandleMessages(self):
        unusedMessages = []
        while len(self.socket.receivedMsgs) != 0:
            message = self.socket.receivedMsgs.pop()
            if message == "!PASSWORDCORRECT":
                self.loggedIn = True
            elif message == "!PASSWORDINCORRECT" or message == "!USERNAMENOTFOUND":
                self.__continueButton.clicked = False
                self.__detailsSent = False
                self.__usernameBox.text = ""
                self.__passwordBox.text = ""
                self.__continueButton.SetText("Continue")

    def HandleInputs(self):
        super().HandleInputs()
        if not self.__continueButton.clicked:
            unusedInputs = []
            while self._inputHandler.inputsPriorityQueue.GetLength() != 0:
                input = self._inputHandler.inputsPriorityQueue.Dequeue()
                if input[1][:6] == "CLICK:":
                    clickLocation = input[1][6:].split(",")
                    clickLocation = (int(clickLocation[0]), int(clickLocation[1]))
                    if self.__continueButton.CheckForCollision(clickLocation):
                        self.__continueButton.clicked = True
                        self.__continueButton.SetText("Checking...")
                    else:
                        for box in self._listOfBoxObjects:
                            if box.CheckForCollisionWithMouse(clickLocation):
                                box.SetActive()
                            else:
                                box.SetInactive()
                elif input[1][:3] == "KD_":
                    key = input[1][3:]
                    for box in self._listOfBoxObjects:
                        if box.isActive:
                            box.AddLetter(key)
                #Sets the other box to be active than the one that is active
                elif input[1] == "TABDOWN":
                    if self.__usernameBox.isActive:
                        self.__usernameBox.SetInactive()
                        self.__passwordBox.SetActive()
                    elif self.__passwordBox.isActive:
                        self.__usernameBox.SetActive()
                        self.__passwordBox.SetInactive()
                elif input[1] == "BACKSPACEDOWN":
                    self._backspace = True
                    self._timeSinceLastBackspace = -200
                elif input[1] == "BACKSPACEUP":
                    self._backspace = False
                else:
                    unusedInputs.append(input)