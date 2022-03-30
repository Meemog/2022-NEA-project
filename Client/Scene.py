import pygame, threading
from InputHandler import InputHandler
from Boxes import InputBox, Button
from Text import Text

#A class for handling scenes
#A scene is made up of buttons, textboxes and displays to render
class Scene:
    #Window is a pygame surface object
    #Screendimensions is a tuple (width, height)
    #Socket is a ClientSocket object from ClientSocket.py
    #bgColour is an RGB value in a tuple e.g. (0,0,0) for black or (255,255,255) for white
    def __init__(self, window, screenDimensions, socket, bgColour = (0,0,0)):
        self.clock = pygame.time.Clock()
        #Used to draw things on
        self.window = window
        #The screen resolution (width, height)
        self.resolution = screenDimensions
        #Clientsocketobject that is used to communicate with the server
        self.socket = socket
        #Background colour for drawing every frame
        self.bgColour = bgColour
        #Stores button objects to render
        self.buttons = []
        #Stores textbox objects to render
        self.boxes = []
        #Stores text objects 
        self.textToRender = []
        #Stores other pygame surface objects to render
        self.surfaces = []
        #Attribute that determines if certain code should run
        self.userQuit = False
        #Attributes if shift, control or alt are being held down
        self.control = False
        self.alt = False
        self.shift = False

        #InputHandler object for checking inputs
        self.inputHandler = InputHandler()

    #Where main logic happens, should be called every frame
    #Needs to check is userQuit is true before running this every frame
    def main(self):
        self.clock.tick()
        self.HandleInput()
        self.CheckMsgs()
        self.Render()

    #Where input handling happens // should be called every frame
    def HandleInput(self):
        self.inputHandler.CheckInputs()
        unusedInputs = []
        while self.inputHandler.inputsPriorityQueue.GetLength() != 0:
            input = self.inputHandler.inputsPriorityQueue.Dequeue()
            if input[1] == "QUIT":
                self.userQuit = True
            elif input[1] == "SHIFTDOWN":
                self.shift = True
            elif input[1] == "SHIFTUP":
                self.shift = False
            elif input[1] == "ALTDOWN":
                self.alt = True
            elif input[1] == "ALTUP":
                self.alt = False
            elif input[1] == "CONTROLDOWN":
                self.control = True
            elif input[1] == "CONTROLUP":
                self.control = False
            else:
                unusedInputs.append(input)

        #Adds unused inputs back to priority queue.
        for input in unusedInputs:
            self.inputHandler.inputsPriorityQueue.Enqueue(input[0], input[1])

        #Highlights buttons when mouse is hovering over buttons
        for button in self.buttons:
            if button.CheckForCollisionWithMouse(pygame.mouse.get_pos()):
                button.SetActive()
            else:
                button.SetInactive()

    #Method that renders buttons, textboxes and displays
    def Render(self):
        self.window.fill(self.bgColour)
        for button in self.buttons:
            button.Render(self.window)
        for box in self.boxes:
            box.Render(self.window)
        for text in self.textToRender:
            text.Render(self.window)
        for surface in self.surfaces:
            surface.Render(self.window)

    def CheckMsgs(self):
        pass

class LoginScreen(Scene):
    def __init__(self, window, screenDimensions, socket, bgColour=(0, 0, 0)):
        super().__init__(window, screenDimensions, socket, bgColour)
        self.loggedIn = False
        self.msgSent = False

        #Making textboxes
        boxColourActive = (50,50,50)
        boxColourInactive = (30,30,30)
        self.textColour = (255,255,255)

        #Finds maximum fontsize that would fiit in 40 pixel height
        fontSize = 1
        font = pygame.font.SysFont("Courier New", fontSize)
        while font.size("Username")[1] < 50 * self.resolution[1] / 1080:
            fontSize += 1
            font = pygame.font.SysFont("Courier New", fontSize)

        font = pygame.font.SysFont("Courier New", fontSize - 1)
        self.font = font

        #InputBoxes (username and password)
        boxSize = (int(1000 * self.resolution[0] / 1920), int(60 * self.resolution[1] / 1080))

        boxTopLeft = (int((self.resolution[0] - boxSize[0]) / 2), int(400 * self.resolution[1] / 1080))
        rectangleUsernameBox = pygame.Rect(boxTopLeft, boxSize)
        self.usernameBox = InputBox(rectangleUsernameBox, boxColourActive, boxColourInactive, self.resolution)

        boxTopLeft = (int((self.resolution[0] - boxSize[0]) / 2), int(540 * self.resolution[1] / 1080))
        rectanglePasswordBox = pygame.Rect(boxTopLeft, boxSize)
        self.passwordBox = InputBox(rectanglePasswordBox, boxColourActive, boxColourInactive, self.resolution, hashed=True)

        #Continue button
        boxSize = (int(400 * self.resolution[0] / 1920), int(60 * self.resolution[1] / 1080))
        buttonTopLeft = (int((self.resolution[0] - boxSize[0]) / 2), int(640 * self.resolution[1] / 1080))
        buttonRect = pygame.Rect(buttonTopLeft, boxSize)
        self.continueButton = Button(buttonRect, boxColourActive, boxColourInactive, self.textColour, text = "Continue")

        #Text to print
        usernameText = Text(self.font, self.textColour, "Username")
        textRender = usernameText.textRender
        usernameTextLocation = ((self.usernameBox.rect.x + 10) * self.resolution[0] / 1920, self.usernameBox.rect.top - (15 + textRender.get_size()[1]) * self.resolution[1] / 1080)
        usernameText.SetLocation(usernameTextLocation)
        self.usernameText = usernameText

        passwordText = Text(self.font, self.textColour, "Password")
        textRender = passwordText.textRender
        passwordTextLocation = ((self.passwordBox.rect.x + 10) * self.resolution[0] / 1920, self.passwordBox.rect.top - (15 + textRender.get_size()[1]) * self.resolution[1] / 1080)
        passwordText.SetLocation(passwordTextLocation)
        self.passwordText = passwordText

        #Boxes and text object lists
        self.activeBox = None
        self.boxes = [self.usernameBox, self.passwordBox]
        self.buttons = [self.continueButton]
        self.textToRender = [self.usernameText, self.passwordText]

        #Used for holding keys down
        self.timeSinceLastAutomaticKeypress = -200
        self.keyBeingHeldDown = None
        self.backspace = False

    def main(self):
        super().main()
        self.AutomaticDeleteLetters()

        #Checks if button is clicked
        if self.continueButton.clicked and not self.msgSent:
            #Sends details to server
            self.usernameBox.SetInactive()
            self.usernameBox.SetInactive()
            username = self.usernameBox.text
            password = self.passwordBox.text
            self.socket.msgsToSend.append(f"!LOGIN:{username},{password}")
            self.msgSent = True
            self.continueButton.SetText("Waiting")

    def HandleInput(self):
        #Does all the inputhandling done for all scenes (quit, control/shift/alt being pressed or released)
        super().HandleInput()
        unusedInputs = []
        while self.inputHandler.inputsPriorityQueue.GetLength() != 0 and not self.continueButton.clicked:
            input = self.inputHandler.inputsPriorityQueue.Dequeue()
            if input[1][:6] == "CLICK:":
                #Converts to list with coordinates
                clickLocation = input[1][6:].split(",")
                #Converts to tuple
                clickLocation = (int(clickLocation[0]), int(clickLocation[1]))

                #To check boxes need to be deselected
                boxActivated = False
                for box in self.boxes:
        