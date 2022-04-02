import pygame

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

    def Render(self, window):
        pygame.draw.rect(window, self._colour, self._rect)

    def AddLetter(self, letter):
        self.text += letter

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

    def SetActive(self):
        self.isActive = True
        self._colour = self._activeColour

    def SetInactive(self):
        self.isActive = False
        self._colour = self._inactiveColour

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

    def CheckIfFinished(self):
        if len(self.text) == len(self.previewText):
            return True
        return False

    def Render(self, window):
        super().Render(window)

        #Copies text so that it can be changed
        text = self.text
        #Cuts text so that it is at most halfway through the box 
        previewText = self.previewText
        while self._font.size(text)[0] > (self._rect.width - 10 * self._resolution[0]) / 2:
            #Splices text for everything after the first letter
            text = text[1:]
            previewText = previewText[1:]
            
        #Cuts end of previewText out until it fits in the box
        while self._font.size(previewText)[0] > self._rect.width - 10 * self._resolution[0]:
            previewText = previewText[:-1]
        
        #Convert to list to assign individual letters
        text = list(text)
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
        textRenderLocation = (int(self._rect.left + 5 * self._resolution[0]), int(self._rect.top + 5 * self._resolution[1]))
        #Converts text to surface objects
        previewText = self._font.render(previewText, True, self._previewTextColour)
        correctText = self._font.render(correctText, True, self.textColour)
        incorrectText = self._font.render(incorrectText, True, self._incorrectTextColour)
        #Draws surface objects onto window
        window.blit(previewText, textRenderLocation)
        window.blit(correctText, textRenderLocation)
        window.blit(incorrectText, textRenderLocation)

class InputBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text, hashed = False) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour, text)
        self.__hashed = hashed

    def Render(self, window):
        super().Render(window)

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

        textRender = self._font.render(textToRender, True, self.textColour)
        textLocation = (self._rect.left + 5 * self._resolution[0], self._rect.top + 10 * self._resolution[1])
        window.blit(textRender, textLocation)
