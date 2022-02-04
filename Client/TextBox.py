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

    #Removes a letter from text and potentially brings back a letter that was previously taken off the screen
    def DeleteLetter(self, control):
        if self.__text != "":
            if control:
                #Removes trailing spaces 
                while self.__text[-1] == " ":
                    self.__text = self.__text[:-1]
                #Removes letters until a space is reached or text has run out
                while self.__text != "" and self.__text[-1] != " ":
                    self.__text = self.__text[:-1]

            else:
                self.__text = self.__text[:-1]   

    def AddLetter(self, letter):
        self.__text += letter

    #Draws the textbox
    def DrawBox(self, window):
        #Length of text is used a lot, this saves some function calls
        lenText = len(self.__text)
        #Cuts front of text so that the end is in the middle
        lettersFromBack = 0
        while self.__font.size(self.__text[-(lettersFromBack + 1):])[0] <= self.__boxSize[0] / 2 and lettersFromBack + 1 <= lenText:
            lettersFromBack += 1
        #Text that is cut to reach the middle of the box
        cutText = self.__text[-lettersFromBack:]

        lettersFromBack2 = lettersFromBack
        #If the preview text isnt empty (Game has started) then it will cut it so that it fits in the textbox
        if self.__previewText != "":
            while self.__font.size(self.__previewText[lenText - lettersFromBack: lettersFromBack2 + 1])[0] <= self.__boxSize[0] - 10:
                lettersFromBack2 += 1

            #Cuts the preview text to fit the whole box
            cutPreviewText = self.__previewText[lenText - lettersFromBack: lettersFromBack2]
            #Cuts the preview text so that it is the same length as cutText
            cutCorrectText = self.__previewText[lenText - lettersFromBack:lenText]
           
            #Replaces correct letters player types with spaces 
            cutText = list(cutText)
            cutCorrectText = list(cutCorrectText)
            for i in range(len(cutText)):
                if cutText[i] == cutPreviewText[i]:
                    cutText[i] = " "
                else:
                    cutText[i] = cutPreviewText[i]
                    cutCorrectText[i] = " "
            cutText = "".join(cutText)
            cutCorrectText = "".join(cutCorrectText)

            #Makes render for both
            previewTextRender = self.__font.render(cutPreviewText, True, self.__previewTextColour)
            cutCorrectTextRender = self.__font.render(cutCorrectText, True, self.__textColour)

            #Renders text that is wrong
            textRender = self.__font.render(cutText, True, self.__textColourWrong)
            textCoords = (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5)

            #Blits the gray text, then the orange text and then the red text
            window.blit(previewTextRender, textCoords)
            window.blit(cutCorrectTextRender, textCoords)
            window.blit(textRender, textCoords)

        elif self.__previewText == "":
            textRender = self.__font.render(cutText, True, self.__previewTextColour)
            window.blit(textRender, (self.__boxCoords[0] + 5, self.__boxCoords[1] + 5))