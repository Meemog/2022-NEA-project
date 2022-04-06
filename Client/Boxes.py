import pygame, math

#A class box that is used for textboxes and inputboxes
class Box:
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text = "") -> None:
        self._rect = rect
        self._font = font
        self._resolution = resolution
        self._activeColour = colourActive
        self._inactiveColour = colourInactive
        #Colour starts inactive
        self.isActive = False
        self._colour = colourInactive
        
        self.text = text
        self.textColour = textColour

    def UpdateRender(self):
        pass

    def Render(self, window):
        pygame.draw.rect(window, self._colour, self._rect)

    def AddLetter(self, letter):
        self.text += letter
        self.UpdateRender()

    def RemoveLetter(self, control):
        if self.text != "":
            if control:
                #Removes trailing spaces 
                while self.text[-1] == " ":
                    self.text = self.text[:-1]
                #Removes letters until a space is reached or text has run out
                while self.text != "" and self.text[-1] != " ":
                    self.text = self.text[:-1]

            else:
                self.text = self.text[:-1]
        self.UpdateRender()

    def SetActive(self):
        self.isActive = True
        self._colour = self._activeColour
        self.UpdateRender()

    def SetInactive(self):
        self.isActive = False
        self._colour = self._inactiveColour
        self.UpdateRender()

    def CheckForCollisionWithMouse(self, mouseLocation):
        if self._rect.collidepoint(mouseLocation):
            return True
        return False

#Main box object for race
class TextBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, previewText, previewTextColour, incorrectTextColour) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour)
        self.previewText = previewText
        self._previewTextColour = previewTextColour
        self._incorrectTextColour = incorrectTextColour

        self.__textRenderLocation = None
        self.__previewTextRender = None
        self.__correctTextRender = None
        self.__incorrectTextRender = None

        self.UpdateRender()

    def SetText(self, newText):
        self.text = newText
        self.UpdateRender()

    def CheckIfFinished(self):
        if len(self.text) == len(self.previewText):
            return True
        return False

    def Render(self, window):
        super().Render(window)
        #Draws surface objects onto window
        window.blit(self.__previewTextRender, self.__textRenderLocation)
        window.blit(self.__correctTextRender, self.__textRenderLocation)
        window.blit(self.__incorrectTextRender, self.__textRenderLocation)

    def UpdateRender(self):
        #Copies text so that it can be changed
        text = self.text
        previewText = self.previewText

        spaceAvailable = int(self._rect.width - 10 * self._resolution[0])

        #Prevents division by 0
        if text != "":
            #Cuts text so that it is at most halfway through the box 
            textWidth = self._font.size(text)[0]
            characterWidth = textWidth / len(text)
            #Only does this if text is longer than the middle of the textbox
            if textWidth > spaceAvailable / 2:
                #Divided by 2 as spaceAvailable is the entire box - 10 pixels
                spaceDifference = textWidth - spaceAvailable / 2
                charactersToRemove = int(math.ceil(spaceDifference / characterWidth))
                #Removes enough characters from front so that it reaches the middle
                text = text[charactersToRemove:]
                previewText = previewText[charactersToRemove:]
            
        previewTextWidth = self._font.size(previewText)[0]
        characterWidth = previewTextWidth / len(previewText)
        #Does same but to make sure previewtext remains in the box
        if spaceAvailable < previewTextWidth:
            spaceDifference = previewTextWidth - spaceAvailable
        charactersToRemove = int(math.ceil(spaceDifference / characterWidth))
        #Removes it from the back of previewtext
        previewText = previewText[:-charactersToRemove]

        #Makes string of correct and incorrect text
        correctText = []
        incorrectText = []
        for i in range(len(text)):
            if text[i] == previewText[i]:
                correctText += previewText[i]
                incorrectText += " "
            else:
                correctText += " " 
                incorrectText += previewText[i]
            
        correctText = "".join(correctText)
        incorrectText = "".join(incorrectText)

        #Location is textbox (x + 5, y + 5)
        self.__textRenderLocation = (int(self._rect.left + 5 * self._resolution[0]), int(self._rect.top + 5 * self._resolution[1]))
        #Converts text to surface objects
        self.__previewTextRender = self._font.render(previewText, True, self._previewTextColour)
        self.__correctTextRender = self._font.render(correctText, True, self.textColour)
        self.__incorrectTextRender = self._font.render(incorrectText, True, self._incorrectTextColour)

class InputBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text, hashed = False) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour, text)
        self.__hashed = hashed
        self.__textLocation = None
        self.__textRender = None
        self.UpdateRender()

    def Render(self, window):
        super().Render(window)
        window.blit(self.__textRender, self.__textLocation)

    def UpdateRender(self):
        if self.__hashed:
            #Makes hashed string
            textToRender = len(self.text) * "*"
        else:
            textToRender = self.text

        textSize = self._font.size(textToRender)

        #Makes text correct size
        while textSize[0] > self._rect.width - 10:
            textToRender = textToRender[1:]
            textSize = self._font.size(textToRender)

        self.__textRender = self._font.render(textToRender, True, self.textColour)
        self.__textLocation = (self._rect.left + 5 * self._resolution[0], self._rect.top + 10 * self._resolution[1])