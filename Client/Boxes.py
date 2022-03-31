import pygame

#A class box that is used for textboxes and inputboxes
class Box:
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text) -> None:
        self._rect = rect
        self._font = font
        self._resolution = resolution
        self._activeColour = colourActive
        self._inactiveColour = colourInactive
        #Colour starts inactive
        self.isActive = False
        self._colour = colourInactive
        
        self._text = text
        self._textColour = textColour

    def Render(self, window):
        pygame.draw.rect(window, self._colour, self._rect)

    def AddLetter(self, letter):
        self._text += letter

    def RemoveLetter(self, control):
        if self._text != "":
            if control:
                #Removes trailing spaces 
                while self._text[-1] == " ":
                    self._text = self._text[:-1]
                #Removes letters until a space is reached or text has run out
                while self._text != "" and self._text[-1] != " ":
                    self._text = self._text[:-1]

            else:
                self._text = self._text[:-1]

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

class TextBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text, previewText, previewTextColour, incorrectTextColour) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour, text)
        self._previewText = previewText
        self._previewTextColour = previewTextColour
        self._incorrectTextColour = incorrectTextColour

    def CheckIfFinished(self):
        if len(self._text) >= len(self._previewText):
            return True
        return False

    def Render(self, window):
        super().Render(window)
        
        if self.CheckIfFinished():
            return 0

        #Length of text is used a lot, this saves some function calls
        lenText = len(self._text)
        #Makes text the same length as 
        text = self._text
        while self._font.size(text) > (self._rect.width - 10 * self._resolution[0]) / 2:
            text = text[1:]

        #If the preview text isnt empty (Game has started) then it will cut it so that it fits in the textbox
        if self._previewText != "":
            #Removes same number of letters from start of previewtext as was removed from text
            previewText = self._previewText
            previewText = previewText[len(self._text) - len(text):]

            #Makes sure that previewText doesn't go out the box
            while self._font.size(previewText) > self._rect.width - 10:
                previewText = previewText[:1]

            #Replaces correct letters player types with spaces 
            cutText = list(text)
            cutCorrectText = list(text)
            cutPreviewText = previewText
            for i in range(len(cutText)):
                if cutText[i] == cutPreviewText[i]:
                    cutText[i] = " "
                else:
                    cutText[i] = cutPreviewText[i]
                    cutCorrectText[i] = " "
                    
            cutText = "".join(cutText)
            cutCorrectText = "".join(cutCorrectText)

            #Makes render for preview text and correctly typed text
            self._previewTextRender = self._font.render(cutPreviewText, True, self._previewTextColour)
            self.cutCorrectTextRender = self._font.render(cutCorrectText, True, self._textColour)

            #Renders incorrectly typed text
            self.cutIncorrectTextRender = self._font.render(cutText, True, self._incorrectTextColour)

        elif self._previewText == "":
            self._textRender = self._font.render(cutText, True, self._previewTextColour)

class InputBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text, hashed = False) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour, text)
        self.__hashed = hashed

    def Render(self, window):
        super().Render(window)

        if self.__hashed:
            #Makes hashed string
            textToRender = len(self._text) * "*"
        else:
            textToRender = self._text

        textSize = self._font.size(textToRender)

        #Makes text correct size
        while textSize[0] > self._rect.width - 10:
            textToRender = textToRender[1:]
            textSize = self._font.size(textToRender)

        textRender = self._font.render(textToRender, True, self._textColour)
        textLocation = (self._rect.left + 5 * self._resolution[0], self._rect.top + 5 * self._resolution[1])
        window.blit(textRender, textLocation)
