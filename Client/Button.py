import pygame
from Text import Text

class Button():
    def __init__(self, rect, colourActive, colourInactive, textColour, text=""):
        self.text = text
        self.rect = rect
        self.colourActive = colourActive
        self.colourInactive = colourInactive
        self.colour = colourInactive

        self.clicked = False
        self.textColour = textColour

        #Finds correct fontsize
        fontSize = 1
        font = pygame.font.SysFont("Calibri", int(fontSize))
        fontRenderSize = font.size(self.text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[0] < self.rect.size[0] and fontRenderSize[1] < self.rect.size[1]:
            fontSize += 1
            font = pygame.font.SysFont("Calibri", int(fontSize))
            fontRenderSize = font.size(self.text)

        self.font = pygame.font.SysFont("Calibri", int(fontSize - 1))

        #Makes Text object
        self.textObject = Text(self.font, self.textColour, self.text)
        textLocation = (int(self.rect.x + (self.rect.width - self.textObject.textRender.get_size()[0]) / 2), int(self.rect.y + (self.rect.height - self.textObject.textRender.get_size()[1]) / 2))
        self.textObject.SetLocation(textLocation)

    def Render(self, window):
        pygame.draw.rect(window, self.colour, self.rect)
        self.textObject.Render(window)

    def SetFont(self, newFont):
        self.font = newFont
        self.textObject.SetFont(newFont)
        textLocation = (int(self.rect.x + (self.rect.width - self.textObject.textRender.get_size()[0]) / 2), int(self.rect.y + (self.rect.height - self.textObject.textRender.get_size()[1]) / 2))
        self.textObject.SetLocation(textLocation)

    def CheckForCollision(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False