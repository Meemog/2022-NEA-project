import pygame
from Text import Text
#A class box that is used for textboxes, inputboxes and buttons
class Box:
    #Rect is a pygame.Rect() object // Can store location and size
    #ColourActive and inactive are RGB values e.g. (0,0,0)
    def __init__(self, rect, colourActive, colourInactive, text = ""):
            self.rect = rect
            self.text = text
            self.colourActive = colourActive
            self.colourInactive = colourInactive
            #Box is unselected by default
            self.colour = colourInactive

    def UpdateRender(self):
        pass

    def Render(self, window):
        pass

    def AddLetter(self, letter):
        pass

    def RemoveLetter(self, control):
        pass

    def SetActive(self):
        self.colour = self.colourActive
        self.UpdateRender()

    def SetInactive(self):
        self.colour = self.colourInactive
        self.UpdateRender()

    #Returns True for active and False for inactive
    def GetState(self):
        if self.colour == self.colourActive:
            return True
        return False

    def SetFont(self, font):
        self.font = font
        self.UpdateRender()

    def SetLocation(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.UpdateRender()

    def SetMiddle(self, pos):
        self.rect.center = pos
        self.UpdateRender()

    def SetText(self, text):
        self.text = text
        self.UpdateRender()
        
    def GetText(self):
        return self.text

    def CheckForCollisionWithMouse(self, mouseLocation):
        if self.rect.collidepoint(mouseLocation):
            return True
        return False

class Button(Box):
    def __init__(self, rect, colourActive, colourInactive, textColour, text=""):
        super().__init__(rect, colourActive, colourInactive, text)
        self.clicked = False
        self.textColour = textColour

        #Finds correct fontsize
        fontSize = 1
        font = pygame.font.SysFont("Courier New", int(fontSize))
        fontRenderSize = font.size(self.text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[0] < self.rect.size[0] and fontRenderSize[1] < self.rect.size[1]:
            fontSize += 1
            font = pygame.font.SysFont("Courier New", int(fontSize))
            fontRenderSize = font.size(self.text)

        self.font = pygame.font.SysFont("Courier New", int(fontSize - 1))

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


class TextBox(Box):
    def __init__(self, rect, colourActive, colourInactive, textColour, wrongTextColour, previewTextColour, font, text=""):
        super().__init__(rect, colourActive, colourInactive, text)
        #Override the parent class setting it to be the text parameter, which is meant to be previewtext
        self.text = ""
        self.textColour = textColour
        self.wrongTextColour = wrongTextColour
        self.previewTextColour = previewTextColour
        #Pygame font objects
        self.font = font
        #Text that is to be dislpayed in the box
        self.previewText = text
        #Placeholders for surface objects
        self.textRender = None
        self.cutCorrectTextRender = None
        self.cutIncorrectTextRender = None
        self.previewTextRender = None
        #Creates actual surface objects
        self.UpdateRender()
        self.textLocation = (self.rect.x + 5, self.rect.y + 5)

    def SetPreviewText(self, newPreviewText):
        self.previewText = newPreviewText
        
    #Control is whether or not control is being held down
    def DeleteLetter(self, control):
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

    def AddLetter(self, letter):
        self.text += letter
        self.UpdateRender()

    def CheckIfFinished(self):
        if len(self.text) >= len(self.previewText):
            return True
        return False

    def UpdateRender(self):
        if self.CheckIfFinished():
            return 0
        #Length of text is used a lot, this saves some function calls
        lenText = len(self.text)
        #Cuts front of text so that the end is in the middle
        lettersFromBack = 0
        while self.font.size(self.text[-(lettersFromBack + 1):])[0] <= self.rect.width / 2 and lettersFromBack + 1 <= lenText:
            lettersFromBack += 1
        #Text that is cut to reach the middle of the box
        cutText = self.text[-lettersFromBack:]

        lettersFromBack2 = lettersFromBack
        #If the preview text isnt empty (Game has started) then it will cut it so that it fits in the textbox
        if self.previewText != "":
            lenPreviewText = len(self.previewText)
            while self.font.size(self.previewText[lenText - lettersFromBack: lettersFromBack2 + 1])[0] <= self.rect.width - 10 and lettersFromBack2 <= lenPreviewText:
                lettersFromBack2 += 1

            #Cuts the preview text to fit the whole box
            cutPreviewText = self.previewText[lenText - lettersFromBack: lettersFromBack2]
            #Cuts the preview text so that it is the same length as cutText
            cutCorrectText = self.previewText[lenText - lettersFromBack:lenText]
           
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

            #Makes render for preview text and correctly typed text
            self.previewTextRender = self.font.render(cutPreviewText, True, self.previewTextColour)
            self.cutCorrectTextRender = self.font.render(cutCorrectText, True, self.textColour)

            #Renders incorrectly typed text
            self.cutIncorrectTextRender = self.font.render(cutText, True, self.wrongTextColour)

        elif self.previewText == "":
            self.textRender = self.font.render(cutText, True, self.previewTextColour)

    def Render(self, window):
        pygame.draw.rect(window, self.colour, self.rect)
        if self.previewText != "":
            #Blits the gray text, then the orange text and then the red text
            window.blit(self.previewTextRender, self.textLocation)
            window.blit(self.cutCorrectTextRender, self.textLocation)
            window.blit(self.cutIncorrectTextRender, self.textLocation)
        elif self.previewText == "" and self.textRender is not None:
            window.blit(self.textRender, self.textLocation)

class InputBox(Box):
    def __init__(self, rect, colourActive, colourInactive, text=""):
        super().__init__(rect, colourActive, colourInactive, text)