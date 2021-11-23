import pygame

class TextBox:
    def __init__(self, boxWidth, boxHeight, boxCoords, boxColourActive, boxColourDormant, textColour, fontSize, textColourWrong = (196, 24, 24)):
        self.__boxSize = (boxWidth, boxHeight)  #Box size (width, height)
        self.__boxCoords = boxCoords    #Box coordinates (x,y)
        self.__boxColourActive = boxColourActive    #Box colour when box is selected
        self.__boxColourDormant = boxColourDormant  #Box colour when box isn't selected
        self.__textColour = textColour  #Text colour for correct letters
        self.__fontSize = fontSize  #Size of the font
        self.__textColourWrong = textColourWrong    #Text colour for wrong letters
        
        self.box = pygame.Rect(self.__boxCoords, self.__boxSize) #Defines rectangle object (pygame)

