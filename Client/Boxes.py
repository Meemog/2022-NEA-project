import pygame

#A class box that is used for textboxes and inputboxes
class Box:
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text) -> None:
        self.rect = rect
        self.font = font
        self.resolution = resolution
        self.activeColour = colourActive
        self.inactiveColour = colourInactive
        #Colour starts inactive
        self.colour = colourInactive
        self.isActive = False
        
        self.text = text
        self.textColour = textColour

    def Render(self, window):
        pass

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
        self.colour = self.activeColour

    def SetInactive(self):
        self.isActive = False
        self.colour = self.inactiveColour

    def CheckForCollisionWithMouse(self, mouseLocation):
        if self.rect.collidepoint(mouseLocation):
            return True
        return False

class TextBox(Box):
    def __init__(self, rect, font, resolution, colourActive, colourInactive, textColour, text, previewText, previewTextColour, incorrectTextColour) -> None:
        super().__init__(rect, font, resolution, colourActive, colourInactive, textColour, text)
        self.previewText = previewText
        self.previewTextColour = previewTextColour
        self.incorrectTextColour = incorrectTextColour

    def CheckIfFinished(self):
        if len(self.text) >= len(self.previewText):
            return True
        return False

    def Render(self):
        if self.CheckIfFinished():
            return 0

        #Length of text is used a lot, this saves some function calls
        lenText = len(self.text)
        #Makes text the same length as 
        text = self.text
        while self.font.size(text) > (self.rect.width - 10 * self.resolution[0]) / 2:
            text = text[1:]

        #If the preview text isnt empty (Game has started) then it will cut it so that it fits in the textbox
        if self.previewText != "":
            #Removes same number of letters from start of previewtext as was removed from text
            previewText = self.previewText
            previewText = previewText[len(self.text) - len(text):]

            #Makes sure that previewText doesn't go out the box
            while self.font.size(previewText) > self.rect.width - 10:
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
            self.previewTextRender = self.font.render(cutPreviewText, True, self.previewTextColour)
            self.cutCorrectTextRender = self.font.render(cutCorrectText, True, self.textColour)

            #Renders incorrectly typed text
            self.cutIncorrectTextRender = self.font.render(cutText, True, self.wrongTextColour)

        elif self.previewText == "":
            self.textRender = self.font.render(cutText, True, self.previewTextColour)

class InputBox(Box):
    def __init__(self, rect, colourActive, colourInactive, text=""):
        super().__init__(rect, colourActive, colourInactive, text)