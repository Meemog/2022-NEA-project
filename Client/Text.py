#Text object that is stored in an array of objects in scene objects
class Text:
    #Font is the pygame font object that it will be rendered with
    #Colour is the RGB value in the form of a tuple
    #Text is the text that needs to be displayed
    #Location is the location of the top left of the render
    def __init__(self, font, colour = (255,255,255), text = "", location = (0,0)):
        self.__font = font
        self.__colour = colour
        self.__text = text
        self.location = location

        #Pygame surface object that can be drawn on other surface objects
        #Having this here reduces number of times it needs to be rendered, better performance
        self.__textRender = self.__font.render(self.__text, True, self.__colour)

    #Changes the text that needs to be rendered
    def SetText(self, newText):
        self.__text = newText
        self.__textRender = self.__font.render(self.__text, True, self.__colour)

    #Changes the colour
    def SetColour(self, newColour):
        self.__colour = newColour
        self.__textRender = self.__font.render(self.__text, True, self.__colour)

    #Changes the font
    def SetFont(self, newFont):
        self.__font = newFont
        self.__textRender = self.__font.render(self.__text, True, self.__colour)

    #Renders the text onto the given window
    def Render(self, window):
        window.blit(self.__textRender, self.location)