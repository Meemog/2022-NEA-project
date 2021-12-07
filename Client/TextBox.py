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
        self.previewTextColour = previewTextColour
        self.__fontSize = fontSize  #Size of the font
        self.__textColourWrong = textColourWrong    #Text colour for wrong letters
        self.__text = ""    #Empty string to add text to later
        self.previewText = previewText
        self.__removedText = [] #List to add removed letters to, so they can be added back when a letter is deleted
        self.missingPreviewText = ""  #Text that is hidden
        self.__removedPreviewText = []
        self.__font = pygame.font.SysFont("Courier New", self.__fontSize)  #sets font to consolas

        self.box = pygame.Rect(self.__boxCoords, self.__boxSize) #Defines rectangle object (pygame)

        while self.__font.size(self.previewText)[0] > self.__boxSize[0] - 10:
            self.missingPreviewText += self.previewText[len(self.previewText) - 1]
            self.previewText = self.previewText[:-1]

    def SetActive(self):
        self.boxColour = self.__boxColourActive
        self.isActive = True

    def SetDormant(self):
        self.boxColour = self.__boxColourDormant
        self.isActive = False

    #Removes a letter from text and potentially brings back a letter that was previously taken off the screen
    def DeleteLetter(self, control):
        #Removes a word if the control key is held down
        deleted = False
        print(control)
        if control:
            while len(self.__text) > 0 and (self.__text[-1] != " " or not deleted): 
                self.missingPreviewText += self.previewText[len(self.previewText) - 1]
                self.previewText = self.previewText[:-1]
                self.__text = self.__text[:-1]
                deleted = True
                if self.__removedText != []:
                    self.__text = self.__removedText.pop() + self.__text

                if self.__removedPreviewText != []:
                    self.previewText = self.__removedPreviewText.pop() + self.previewText

        else:
            self.__text = self.__text[:-1]
            self.missingPreviewText += self.previewText[len(self.previewText) - 1]
            self.previewText = self.previewText[:-1]
            if self.__removedText != []:
                self.__text = self.__removedText.pop() + self.__text

            if self.__removedPreviewText != []:
                self.previewText = self.__removedPreviewText.pop() + self.previewText

    def AddLetter(self, letter):
        #Checks if letter added is the same as next letter in preview text
        if letter == self.previewText[len(self.__text)]:
            self.__text += " "
        else:
            self.__text += self.previewText[len(self.__text)]
        
    #Draws the textbox
    def DrawBox(self, window):
        #Removes text when letter is typed and the cursor has reached the middle of the screen
        while self.__font.size(self.__text)[0] > self.__boxSize[0] / 2:
            self.__removedText.append(self.__text[0])   #Adds front letter to the removed text list when the typed letters get to the middle of the box 
            self.__text = self.__text[1:]   #Removes front letter

            self.__removedPreviewText.append(self.previewText[0]) #Adds front letter to removed list
            self.previewText = self.previewText[1:] #Removes front letter

        while self.__font.size(self.previewText + self.missingPreviewText[-1])[0] <= self.__boxSize[0] - 10:
            self.previewText += self.missingPreviewText[-1]
            self.missingPreviewText = self.missingPreviewText[:-1]
            
        #Blits (draws) the preview text
        textRender = self.__font.render(self.previewText, True, self.previewTextColour)
        window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

        #Blits the preview text in the right colour
        cutPreviewText = self.previewText[:len(self.__text)]
        textRender = self.__font.render(cutPreviewText, True, self.__textColour)
        window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

        #Blits the incorrect letters
        textRender = self.__font.render(self.__text, True, self.__textColourWrong)
        window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))
