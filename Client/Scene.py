import pygame, threading, socket
from ClientSocket import ClientSocket
from InputHandler import InputHandler
from Boxes import InputBox, TextBox
from Button import Button
from Text import Text

class Scene:
    def __init__(self, window, resolution, socket : ClientSocket = None) -> None:
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

        #Helps performance to have a surface object instead of filling the entire screen every frame
        self._backgroundSurface = pygame.Surface((int(self._resolution[0] * 1920), int(self._resolution[1] * 1080)))
        self._backgroundSurface.fill((0,0,0))

    def main(self):
        self._clock.tick()
        self._timeSinceLastBackspace += self._clock.get_time()

        self._HandleInputs()

        #Automatic removal of text every 50 milliseconds
        if self._backspace and self._timeSinceLastBackspace >= 50:
            for box in self._listOfBoxObjects:
                if box.isActive:
                    box.RemoveLetter(self._ctrl)
            self._timeSinceLastBackspace = 0

        for buttonObject in self._listOfButtonObjects:
            if buttonObject.CheckForCollision(pygame.mouse.get_pos()):
                buttonObject.SetActive()
            else:
                buttonObject.SetInactive()

        self._Render()

    def _Render(self):
        self._window.blit(self._backgroundSurface, (0,0))
        for box in self._listOfBoxObjects:
            box.Render(self._window)
        for button in self._listOfButtonObjects:
            button.Render(self._window)
        for textObject in self._listOfTextObjects:
            textObject.Render(self._window)

    def _HandleInputs(self):
        self._inputHandler.CheckInputs()
        i = 0
        while i < len(self._inputHandler.inputsList):            
            if self._inputHandler.inputsList[i] == "QUIT":
                self.userQuit = True
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "SHIFTDOWN":
                self._shift = True
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "SHIFTUP":
                self._shift = False
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "ALTDOWN":
                self._alt = True
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "ALTUP":
                self._alt = False
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "CONTROLDOWN":
                self._ctrl = True
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "CONTROLUP":
                self._ctrl = False
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "BACKSPACEDOWN":
                self._backspace = True
                self._timeSinceLastBackspace = -200
                for box in self._listOfBoxObjects:
                    if box.isActive:
                        box.RemoveLetter(self._ctrl)
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i] == "BACKSPACEUP":
                self._backspace = False
                self._inputHandler.inputsList.pop(i)
            else:
                i += 1

#Displays text that changes in the middle of the screen
class ConnectionScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.connected = False

        #Used for changing the number of dots in the text
        self.__timeSinceLastMessageUpdate = 0
        self.__numberOfDots = 0

        self.__font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))

        textSize = self.__font.size("Connecting to server...")
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))

        self.__textToRender = "Connecting to server"
        self.__textObject = Text(self.__font, text=self.__textToRender, location=textLocation)

        self._listOfTextObjects = [self.__textObject]
        
        #Used for connecting to server
        self.__serverSearchThread = threading.Thread(target=self.__ConnectToServer, daemon=True)
        self.__serverSearchThread.start()

    def main(self):
        super().main()
        self.__timeSinceLastMessageUpdate += self._clock.get_time()
        if self.__timeSinceLastMessageUpdate >= 700:
            self.__textToRender = "Connecting to server" + "." * self.__numberOfDots
            self.__textObject.SetText(self.__textToRender)
            self.__numberOfDots += 1
            if self.__numberOfDots == 4:
                self.__numberOfDots = 0
            self.__timeSinceLastMessageUpdate = 0

    def __ConnectToServer(self):
        while not self.connected:
            try:
                self.socket = ClientSocket()
                self.connected = True
            except socket.error:
                pass

    def _HandleInputs(self):
        super()._HandleInputs()
        #Empties list so inputs dont carry over to next scene
        self._inputHandler.inputsList = []

#Displays username and password input boxes
class LoginScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.loggedIn = False
        self.__detailsSent = False

        inputBoxFont = pygame.font.SysFont("Courier New", int(36 * self._resolution[1]))

        #Need 2 inputboxes, 2 text and 1 button
        inputBoxSize = (int(625 * self._resolution[0]), int(60 * self._resolution[1]))
        #Button needs to be centred and 400 pixels down
        usernameBoxLocation = (int((self._resolution[0] * 1920 - inputBoxSize[0]) / 2), int(400 * self._resolution[1]))
        passwordBoxLocation = (int((self._resolution[1] * 1920 - inputBoxSize[0]) / 2), int(540 * self._resolution[1]))
        usernameRect = pygame.Rect(usernameBoxLocation[0], usernameBoxLocation[1], inputBoxSize[0], inputBoxSize[1])
        passwordRect = pygame.Rect(passwordBoxLocation[0], passwordBoxLocation[1], inputBoxSize[0], inputBoxSize[1])
        self.__usernameBox = InputBox(usernameRect, inputBoxFont, self._resolution, (40,40,40), (25,25,25), (255,255,255), "")
        self.__passwordBox = InputBox(passwordRect, inputBoxFont, self._resolution, (40,40,40), (25,25,25), (255,255,255), "", hashed=True)

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
        if self.__continueButton.clicked:
            if not self.__detailsSent:
                username = self.__usernameBox.text
                password = self.__passwordBox.text
                self.socket.msgsToSend.append(f"!LOGIN:{username},{password}")
                self.__detailsSent = True
            else:
                self.__HandleMessages()

    def __HandleMessages(self):
        unusedMessages = []
        while len(self.socket.receivedMsgs) != 0:
            message = self.socket.receivedMsgs.pop()
            if message == "!PASSWORDCORRECT" or message == "!ALREADYLOGGEDIN":
                print("Logged in")
                self.loggedIn = True
            elif message == "!PASSWORDINCORRECT" or message == "!USERNAMENOTFOUND":
                self.__continueButton.clicked = False
                self.__detailsSent = False
                self.__usernameBox.text = ""
                self.__passwordBox.text = ""
                self.__continueButton.SetText("Continue")

    def _HandleInputs(self):
        super()._HandleInputs()
        if not self.__continueButton.clicked:
            i = 0
            while i < len(self._inputHandler.inputsList):
                if self._inputHandler.inputsList[i][:6] == "CLICK:":
                    clickLocation = self._inputHandler.inputsList[i][6:].split(",")
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
                    self._inputHandler.inputsList.pop(i)
                elif self._inputHandler.inputsList[i][:3] == "KD_":
                    key = self._inputHandler.inputsList[i][3:]
                    for box in self._listOfBoxObjects:
                        if box.isActive:
                            box.AddLetter(key)
                    self._inputHandler.inputsList.pop(i)
                #Sets the other box to be active than the one that is active
                elif self._inputHandler.inputsList[i] == "TABDOWN":
                    if self.__usernameBox.isActive:
                        self.__usernameBox.SetInactive()
                        self.__passwordBox.SetActive()
                    elif self.__passwordBox.isActive:
                        self.__usernameBox.SetActive()
                        self.__passwordBox.SetInactive()
                    self._inputHandler.inputsList.pop(i)
                elif self._inputHandler.inputsList[i] == "RETURNDOWN":
                    self.__continueButton.clicked = True
                    self.__continueButton.SetText("Checking...")
                    self._inputHandler.inputsList.pop(i)
                elif self._inputHandler.inputsList[i] == "RETURNUP":
                    #Returnup shouldnt be added back to queue
                    self._inputHandler.inputsList.pop(i)
                else:
                    i += 1

#Displays main menu for user to make choice what to see
class MainMenu(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.userChoice = None
        colourActive = (40,40,40)
        colourInactive = (25,25,25)
        textColour = (255,255,255)

        self.__titleFont = pygame.font.SysFont("Calibri", int(140 * self._resolution[1]))

        boxSize = (int(2/5 * self._resolution[0] * 1920), int(150 * self._resolution[1]))
        boxX = int((self._resolution[0] * 1920 - boxSize[0]) / 2)

        #Needs 4 buttons and a title text
        playButtonRect = pygame.Rect(boxX, int(320 * self._resolution[1]), boxSize[0], boxSize[1])
        statisticsButtonRect = pygame.Rect(boxX, int(500 * self._resolution[1]), boxSize[0], boxSize[1])
        settingsButtonRect = pygame.Rect(boxX, int(680 * self._resolution[1]), boxSize[0], boxSize[1])
        quitButtonRect = pygame.Rect(boxX, int(860 * self._resolution[1]), boxSize[0], boxSize[1])
    
        self.__playButton = Button(playButtonRect, colourActive, colourInactive, textColour, text="Play")
        self.__statisticsButton = Button(statisticsButtonRect, colourActive, colourInactive, textColour, text="Statistics")
        self.__settingsButton = Button(settingsButtonRect, colourActive, colourInactive, textColour, text = "Settings")
        self.__quitButton = Button(quitButtonRect, colourActive, colourInactive, textColour, text="Quit")

        self._listOfButtonObjects = [self.__playButton, self.__statisticsButton, self.__settingsButton, self.__quitButton]

        #Need title text
        titleSize = self.__titleFont.size("SpeedTyper")
        titleLocation = (int((self._resolution[0] * 1920 - titleSize[0]) / 2), int(160 * self._resolution[1]))
        self.__titleText = Text(self.__titleFont, text="SpeedTyper", location=titleLocation, colour=(255,165,0))
        
        self._listOfTextObjects = [self.__titleText]

    def main(self):
        super().main()
        for button in self._listOfButtonObjects:
            if button.clicked:
                if button.text == "Quit":
                    self.userQuit = True
                else:
                    self.userChoice = button.text

    def _HandleInputs(self):
        super()._HandleInputs()
        i = 0
        while i < len(self._inputHandler.inputsList):
            if self._inputHandler.inputsList[i][:6] == "CLICK:":
                clickLocation = self._inputHandler.inputsList[i][6:].split(",")
                clickLocation = (int(clickLocation[0]), int(clickLocation[1]))
                for button in self._listOfButtonObjects:
                    if button.CheckForCollision(clickLocation):
                        button.clicked = True
                self._inputHandler.inputsList.pop(i)
            else:
                i += 1

#Displays message that they are in queue
class MatchmakingScreen(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.gameFound = False
        self.userClickedBackButton = False

        #Used for changing the number of dots in the text
        self.__timeSinceLastMessageUpdate = 0
        self.__numberOfDots = 0

        self.__font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))

        #Text for the screen
        textSize = self.__font.size("Looking for game...")
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))

        self.__textToRender = "Looking for game"
        self.__textObject = Text(self.__font, text=self.__textToRender, location=textLocation)

        self._listOfTextObjects = [self.__textObject]

        #Button to dequeue
        backButtonSize = (400 * self._resolution[0], 60 * self._resolution[1])
        #Button needs to be centred and 680 pixels down
        backButtonLocation = ((self._resolution[0] * 1920 - backButtonSize[0]) / 2, 680 * self._resolution[1])
        backButtonRect = pygame.Rect(backButtonLocation[0], backButtonLocation[1], backButtonSize[0], backButtonSize[1])
        self.backButton = Button(backButtonRect, (40,40,40), (25,25,25), (255,255,255), text="Back")

        self._listOfButtonObjects = [self.backButton]

    def main(self):
        super().main()
        self.__TextAnimation()
        self.__HandleMessages()

    def __HandleMessages(self):
        i = 0
        while i < len(self.socket.receivedMsgs):
            if self.socket.receivedMsgs[i] == "!GAMEFOUND":
                self.gameFound = True
                self.socket.receivedMsgs.pop(i)
            else:
                i += 1

    def _HandleInputs(self):
        super()._HandleInputs()
        i = 0
        while i < len(self._inputHandler.inputsList):
            if self._inputHandler.inputsList[i][:6] == "CLICK:":
                clickLocation = self._inputHandler.inputsList[i][6:].split(",")
                clickLocation = (int(clickLocation[0]), int(clickLocation[1]))
                for button in self._listOfButtonObjects:
                    if button.CheckForCollision(clickLocation):
                        button.clicked = True
                        if button.text == "Back":
                            self.userClickedBackButton = True
                self._inputHandler.inputsList.pop(i)
            else:
                i += 1

    def __TextAnimation(self):
        #Used for animation of looking for game text
        self.__timeSinceLastMessageUpdate += self._clock.get_time()
        if self.__timeSinceLastMessageUpdate >= 700:
            self.__textToRender = "Looking for game" + "." * self.__numberOfDots
            self.__textObject.SetText(self.__textToRender)
            self.__numberOfDots += 1
            if self.__numberOfDots == 4:
                self.__numberOfDots = 0
            self.__timeSinceLastMessageUpdate = 0


#Scene for timer
class TimerScene(Scene):
    def __init__(self, window, resolution, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.timerFinished = False
        self.__font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))

        #Text for the screen
        textSize = self.__font.size("Waiting for timer")
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))
        self.__textObject = Text(self.__font, text="Waiting for timer", location=textLocation)
        self._listOfTextObjects = [self.__textObject]

    def main(self):
        super().main()
        self.__HandleMessages()

    def __HandleMessages(self):
        i = 0
        while i < len(self.socket.receivedMsgs):
            if self.socket.receivedMsgs[i][:10] == "!TIMELEFT:":
                timeLeft = self.socket.receivedMsgs[i][10:]
                #Updates timer on screen
                self.__UpdateTextObject(timeLeft)
                if int(timeLeft) == 0:
                    self.timerFinished = True
                #Removes message from list
                self.socket.receivedMsgs.pop(i)
            else:
                i += 1

    #Updates text and location to be centred
    def __UpdateTextObject(self, newText):
        textSize = self.__font.size(newText)
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))
        self.__textObject.SetText(newText)
        self.__textObject.location = textLocation

    def _HandleInputs(self):
        super()._HandleInputs()
        #Empties inputs list so they dont carry over to the next scene
        self._inputHandler.inputsList = []

class RaceScene(Scene):
    def __init__(self, window, resolution, previewText, socket=None) -> None:
        super().__init__(window, resolution, socket)
        self.playerFinished = False
        self.gameOver = False
        #Colours for textbox        
        colourActive = (40,40,40)
        colourInactive = (25,25,25)
        previewTextColour = (160,160,160)
        incorrectTextColour = (255,0,0)

        #Main textbox
        textBoxFont = pygame.font.SysFont("Courier New", int(42 * self._resolution[1]))

        textBoxSize = (self._resolution[0] * 1920 * 2/5, 50 * self._resolution[1])
        textBoxLocation = ((self._resolution[0] * 1920 - textBoxSize[0]) / 2, 250 * self._resolution[1])
        textBoxRect = pygame.Rect(textBoxLocation[0], textBoxLocation[1], textBoxSize[0], textBoxSize[1])
        self.__textBox = TextBox(textBoxRect, textBoxFont, self._resolution, colourActive, colourInactive, (38, 191, 79), previewText, previewTextColour, incorrectTextColour)

        #Other player textbox
        #Box is 250 pixels above the bottom of the screen
        textBoxLocation = ((self._resolution[0] * 1920 - textBoxSize[0]) / 2, self._resolution[1] * 1080 - (250 + textBoxSize[1]) * self._resolution[1])
        textBoxRect = pygame.Rect(textBoxLocation[0], textBoxLocation[1], textBoxSize[0], textBoxSize[1])
        self.__opponentTextBox = TextBox(textBoxRect, textBoxFont, self._resolution, colourActive, colourInactive, (38, 191, 79), previewText, previewTextColour, incorrectTextColour)

        self._listOfBoxObjects = [self.__textBox, self.__opponentTextBox]

        #Needs to be attribute as it will be used to change text later on
        self.timerFinished = False
        self.__font = pygame.font.SysFont("Calibri", int(72 * self._resolution[1]))

        #Text for timer
        textSize = self.__font.size("30")
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))
        self.__textObject = Text(self.__font, text="30", location=textLocation)
        self._listOfTextObjects = [self.__textObject]

    def main(self):
        super().main()
        self.__HandleMessages()

    def SetPreviewText(self, previewText):
        self.__textBox.previewText = previewText

    def __HandleMessages(self):
        #Code for receiving messages from server
        i = 0
        while i < len(self.socket.receivedMsgs):
            if self.socket.receivedMsgs[i][:10] == "!TIMELEFT:":
                timeLeft = self.socket.receivedMsgs[i][10:]
                #Updates timer on screen
                self.__UpdateTextObject(timeLeft)
                if timeLeft == 0:
                    self.timerFinished = True
                #Removes message from list
                self.socket.receivedMsgs.pop(i)
            #Other player's text
            elif self.socket.receivedMsgs[i][:17] == "!OTHERPLAYERTEXT:":
                text = self.socket.receivedMsgs[i][17:]
                self.__opponentTextBox.text = text
                self.socket.receivedMsgs.pop(i)
            #Time has run out, client has to send text
            elif self.socket.receivedMsgs[i] == "!GAMECOMPLETE":
                self.socket.msgsToSend.append(f"!FINALTEXT:{self.__textBox.text}")
                self.timerFinished = True
                self.socket.receivedMsgs.pop(i)
            #Server received both player's final text and game has finished
            #Emphasis on the D in completed, not the same as complete as it is for server asking for player's final text
            elif self.socket.receivedMsgs[i] == "!GAMECOMPLETED":
                self.gameOver = True
                self.socket.receivedMsgs.pop(i)

            else:
                i += 1

    #Updates text and location to be centred
    def __UpdateTextObject(self, newText):
        textSize = self.__font.size(newText)
        textLocation = (int((self._resolution[0] * 1920 - textSize[0]) / 2), int((self._resolution[1] * 1080 - textSize[1]) / 2))
        self.__textObject.location = textLocation
        self.__textObject.SetText(newText)

    def _HandleInputs(self):
        super()._HandleInputs()
        i = 0
        while i < len(self._inputHandler.inputsList):
            if self._inputHandler.inputsList[i][:3] == "KD_":
                #This needs to be indented in order to still delete the input from the queue
                if not self.playerFinished:
                    if self.__textBox.isActive:
                        letter = self._inputHandler.inputsList[i][3:]
                        self.__textBox.AddLetter(letter)
                        self.socket.msgsToSend.append(f"!TEXT:{self.__textBox.text}")
                        if self.__textBox.CheckIfFinished():
                            self.playerFinished = True
                self._inputHandler.inputsList.pop(i)
            elif self._inputHandler.inputsList[i][:6] == "CLICK:":
                clickLocation = self._inputHandler.inputsList[i][6:].split(",")
                clickLocation = (int(clickLocation[0]), int(clickLocation[1]))
                for box in self._listOfBoxObjects:
                    #Opponent box cannot be activated otherwise the opponent's text would also be deleted when backspace is pressed
                    if box.CheckForCollisionWithMouse(clickLocation) and box != self.__opponentTextBox:
                        box.SetActive()
                    else:
                        box.SetInactive()
                self._inputHandler.inputsList.pop(i)
            else:
                i += 1

# #Used for testing
# import ctypes, pygame

# user32 = ctypes.windll.user32
# #Prevents the screen from scaling with windows resolution scale
# #System -> Display -> Scale and Layout
# user32.SetProcessDPIAware()

# window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# pygame.display.set_caption("SpeedTyper")
# pygame.font.init()

# res = pygame.display.Info()
# res = (res.current_w / 1920, res.current_h / 1080)

# text = "Hello this is a preview text"

# thisRace = Race(window, res, text)
# while not thisRace.userQuit:
#     thisRace.main()
#     pygame.display.update()

# pygame.font.quit()
# pygame.quit()