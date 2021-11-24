import pygame

class TextBox:
    def __init__(self, boxWidth, boxHeight, boxCoords, boxColourActive, boxColourDormant, textColour, fontSize, previewText, previewTextColour, textColourWrong = (196, 24, 24)):
        self.__boxSize = (boxWidth, boxHeight)  #Box size (width, height)
        self.__boxCoords = boxCoords    #Box coordinates (x,y)
        self.__boxColourActive = boxColourActive    #Box colour when box is selected
        self.__boxColourDormant = boxColourDormant  #Box colour when box isn't selected
        self.isActive = False
        self.boxColour = self.__boxColourDormant
        self.__textColour = textColour  #Text colour for correct letters
        self.__previewTextColour = previewTextColour
        self.__fontSize = fontSize  #Size of the font
        self.__textColourWrong = textColourWrong    #Text colour for wrong letters
        self.__text = ""    #Empty string to add text to later
        self.__previewText = previewText
        self.__removedText = [] #List to add removed letters to, so they can be added back when a letter is deleted
        self.__missingPreviewText = ""  #Text that is hidden
        self.__removedPreviewText = []
        self.__font = pygame.font.SysFont("consolas", self.__fontSize)  #sets font to consolas

        self.box = pygame.Rect(self.__boxCoords, self.__boxSize) #Defines rectangle object (pygame)

        while self.__font.size(self.__previewText)[0] > self.__boxSize[0] - 10:
            self.__missingPreviewText += self.__previewText[len(self.__previewText) - 1]
            self.__previewText = self.__previewText[:-1]

    def SetActive(self):
        self.boxColour = self.__boxColourActive
        self.isActive = True

    def SetDormant(self):
        self.boxColour = self.__boxColourDormant
        self.isActive = False

    def DeleteLetter(self):
        self.__text = self.__text[:-1]
        if self.__removedText != []:
            self.__text = self.__removedText.pop() + self.__text

        if self.__removedPreviewText != []:
            self.__previewText = self.__removedPreviewText.pop() + self.__previewText
        
    def AddLetter(self, letter):
        self.__text += letter
        
    def DrawBox(self, window):
        while self.__font.size(self.__text)[0] > self.__boxSize[0] / 2:
            self.__removedText.append(self.__text[0])   #Adds front letter to the removed text list when the typed letters get to the middle of the box 
            self.__text = self.__text[1:]   #Removes front letter

            self.__removedPreviewText.append(self.__previewText[0]) #Adds front letter to removed list
            self.__previewText = self.__previewText[1:] #Removes front letter

        while self.__font.size(self.__previewText + self.__missingPreviewText[-1])[0] <= self.__boxSize[0] - 10:
            self.__previewText += self.__missingPreviewText[-1]
            self.__missingPreviewText = self.__missingPreviewText[:-1]
            
        textRender = self.__font.render(self.__previewText, True, self.__previewTextColour)
        window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

        textRender = self.__font.render(self.__text, True, self.__textColour)
        window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))