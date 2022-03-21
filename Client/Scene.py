#A class for handling scenes
#A scene is made up of buttons, textboxes and displays to render
class Scene:
    #Window is a pygame surface object
    #Screendimensions is a tuple (width, height)
    #Socket is a ClientSocket object from ClientSocket.py
    #bgColour is an RGB value in a tuple e.g. (0,0,0) for black or (255,255,255) for white
    def __init__(self, window, screenDimensions, socket, bgColour = (0,0,0)):
        #Used to draw things on
        self.window = window
        #The screen resolution (width, height)
        self.__resolution = screenDimensions
        #Clientsocketobject that is used to communicate with the server
        self.socket = socket
        #Background colour for drawing every frame
        self.bgColour = bgColour
        #Stores button objects to render
        self.buttons = []
        #Stores textbox objects to render
        self.textBoxes = []
        #Stores text objects 
        self.text = []
        #Stores other pygame surface objects to render
        self.surfaces = []
        #Attribute that determines if certain code should run
        self.userQuit = False

    #Where main logic happens
    def main(self):
        pass

    #Where input handling happens // should be called every frame
    def HandleInput(self):
        pass

    #Method that renders buttons, textboxes and displays
    def Render(self):
        self.window.surfaces(self.bgColour)
        for button in self.buttons:
            button.Render(self.window)
        for textBox in self.textBoxes:
            textBox.Render(self.window)
        for text in self.text:
            text.Render(self.window)
        for surface in self.surfaces:
            surface.Render(self.window)
            