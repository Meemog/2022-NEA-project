from typing import Text
import pygame

class TextBox:
    def __init__(self, boxWidth, boxHeight, boxCoords, boxColourActive, boxColourDormant, textColour, font, previewTextColour, textColourWrong = (196, 24, 24)):
        self.__boxSize = (boxWidth, boxHeight)  #Box size (width, height)
        self.__boxCoords = boxCoords    #Box coordinates (x,y)
        self.__boxColourActive = boxColourActive    #Box colour when box is selected
        self.__boxColourDormant = boxColourDormant  #Box colour when box isn't selected
        self.isActive = False
        self.boxColour = self.__boxColourDormant
        self.__textColour = textColour  #Text colour for correct letters
        self.__previewTextColour = previewTextColour
        self.__textColourWrong = textColourWrong    #Text colour for wrong letters
        self.__text = ""    #Empty string to add text to later
        self.__previewText = ""
        self.__removedText = [] #List to add removed letters to, so they can be added back when a letter is deleted
        self.__missingPreviewText = ""  #Text that is hidden
        self.__removedPreviewText = []
        self.__font = font

        self.box = pygame.Rect(self.__boxCoords, self.__boxSize) #Defines rectangle object (pygame)

    def SetActive(self):
        self.boxColour = self.__boxColourActive
        self.isActive = True

    def SetDormant(self):
        self.boxColour = self.__boxColourDormant
        self.isActive = False

    #Sets the previewText to text
    def SetPreviewText(self, text):
        self.__previewText = text
        self.__text = ""
        #Cuts preview text to fit the screen
        while self.__font.size(self.__previewText)[0] > self.__boxSize[0] - 10:
            self.__missingPreviewText += self.__previewText[len(self.__previewText) - 1]
            self.__previewText = self.__previewText[:-1]

    #Removes a letter from text and potentially brings back a letter that was previously taken off the screen
    def DeleteLetter(self, control):
        #Removes a word if the control key is held down
        deleted = False
        print(control)
        if control:
            while len(self.__text) > 0 and (self.__text[-1] != " " or not deleted): 
                self.__missingPreviewText += self.__previewText[len(self.__previewText) - 1]
                self.__previewText = self.__previewText[:-1]
                self.__text = self.__text[:-1]
                deleted = True
                if self.__removedText != []:
                    self.__text = self.__removedText.pop() + self.__text

                if self.__removedPreviewText != []:
                    self.__previewText = self.__removedPreviewText.pop() + self.__previewText

        else:
            self.__text = self.__text[:-1]
            if self.__previewText != "":
                self.__missingPreviewText += self.__previewText[len(self.__previewText) - 1]
                self.__previewText = self.__previewText[:-1]
                if self.__removedText != []:
                    self.__text = self.__removedText.pop() + self.__text

                if self.__removedPreviewText != []:
                    self.__previewText = self.__removedPreviewText.pop() + self.__previewText

    def AddLetter(self, letter):
        if self.__previewText != "":
            #Checks if letter added is the same as next letter in preview text
            if letter == self.__previewText[len(self.__text)]:
                self.__text += " "
            else:
                self.__text += self.__previewText[len(self.__text)]
        else:
            self.__text += letter

    #Draws the textbox
    def DrawBox(self, window):
        #Removes text when letter is typed and the cursor has reached the middle of the screen
        while self.__font.size(self.__text)[0] > self.__boxSize[0] / 2:
            self.__removedText.append(self.__text[0])   #Adds front letter to the removed text list when the typed letters get to the middle of the box 
            self.__text = self.__text[1:]   #Removes front letter

        #If the preview text isnt empty (Game has started) then it will cut it so that it fits in the textbox
        if self.__previewText != "":
            #Removes text that goes out of the textbox
            while self.__font.size(self.__previewText + self.__missingPreviewText[-1])[0] <= self.__boxSize[0] - 10:
                self.__previewText += self.__missingPreviewText[-1]
                self.__missingPreviewText = self.__missingPreviewText[:-1]
                
            #Blits (draws) the preview text
            textRender = self.__font.render(self.__previewText, True, self.__previewTextColour)
            window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

            #Blits the preview text in the right colour for how long the text written by player is
            cutPreviewText = self.__previewText[:len(self.__text)]
            textRender = self.__font.render(cutPreviewText, True, self.__textColour)
            window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

            #Blits the incorrect letters in a different colour
            textRender = self.__font.render(self.__text, True, self.__textColourWrong)
            window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))

        elif self.__previewText == "":
            textRender = self.__font.render(self.__text, True, self.__textColour)
            window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))