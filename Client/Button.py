import pygame
from Text import Text

class Button():
    def __init__(self, rect, colourActive, colourInactive, textColour, text=""):
        self.text = text
        self.__rect = rect
        self.__activeColour = colourActive
        self.__inactiveColour = colourInactive
        self.__colour = colourInactive

        self.clicked = False
        self.textColour = textColour

        #Finds correct fontsize
        fontSize = 1
        font = pygame.font.SysFont("Calibri", int(fontSize))
        fontRenderSize = font.size(self.text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[0] < self.__rect.size[0] and fontRenderSize[1] < self.__rect.size[1]:
            fontSize += 1
            font = pygame.font.SysFont("Calibri", int(fontSize))
            fontRenderSize = font.size(self.text)

        self.__font = pygame.font.SysFont("Calibri", int(fontSize - 1))

        #Makes Text object
        textSize = self.__font.size(self.text)
        textLocation = (int(self.__rect.left + (self.__rect.width - textSize[0]) / 2), int(self.__rect.top + (self.__rect.height - textSize[1]) / 2))
        self.textObject = Text(self.__font, self.textColour, self.text, location=textLocation)

    def Render(self, window):
        pygame.draw.rect(window, self.__colour, self.__rect)
        self.textObject.Render(window)

    def SetText(self, newText):
        self.text = newText
        self.textObject.SetText(newText)

    def SetFont(self, newFont):
        self.__font = newFont
        self.textObject.SetFont(newFont)
        textLocation = (int(self.__rect.x + (self.__rect.width - self.textObject.textRender.get_size()[0]) / 2), int(self.__rect.y + (self.__rect.height - self.textObject.textRender.get_size()[1]) / 2))
        self.textObject.SetLocation(textLocation)

    def SetActive(self):
        self.__colour = self.__activeColour
    
    def SetInactive(self):
        self.__colour = self.__inactiveColour

    def CheckForCollision(self, pos):
        if self.__rect.collidepoint(pos):
            return True
        return False