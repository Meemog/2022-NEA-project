import pygame

class InputBox:
    #Does not support changing the size of the rectangle
    def __init__(self, textColour, colourActive, colourDormant, hashedOut, rectangle, dispHeight):
        #This is where the text that needs to be displayed is stored
        self.text = ""
        self.__textColour = textColour
        #The box's colour, originally set to inactive
        self.__colour = colourDormant
        #Determines whether or not the box is selected
        self.isActive = False
        #Colour for when the box is selected or unselected
        self.__colourActive = colourActive
        self.__colourDormant = colourDormant
        #Determines if the text should be displayed
        self.__hashedOut = hashedOut
        #Used for some calculations
        self.__size = rectangle.size
        self.__location = (rectangle.x, rectangle.y)
        self.rectangle = rectangle

        #Finds the largest font size that can fit in the box, given its size
        fontSize = 999
        font = pygame.font.SysFont("Courier New", int(dispHeight * fontSize/1080))
        fontRenderSize = font.size(self.text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[1] > self.__size[1]:
            fontSize -= 1
            font = pygame.font.SysFont("Courier New", int(dispHeight * fontSize/1080))
            fontRenderSize = font.size(self.text)

        #Font object with correct size
        self.__font = font

    #Renders the box on window
    def DrawBox(self, window):
        #Draws the rectangle with the right colour
        pygame.draw.rect(window, self.__colour, self.rectangle)

        #Converts text to be starred out if it is meant to be
        if self.__hashedOut:
            text = "*"*len(self.text)

        else:
            text = self.text

        #Finds how many letters it needs to cut off from the front for the text to fit in the box
        lettersFromBack = len(text)
        #While the rendered version of text with lettersFromBack number of letters from the back is bigger than the textbox
        while self.__font.size(text[-lettersFromBack:])[0] > self.__size[0] - 10:
            lettersFromBack -= 1

        #Renders the text but cuts off the right amount from the back
        textRender = self.__font.render(text[-lettersFromBack:], True, self.__textColour)
        window.blit(textRender, (self.__location[0] + 5, self.__location[1] + 5))
    
    #Checks if location is on the box
    def CheckIfClicked(self, location):
        if self.rectangle.collidepoint(location):
            return True

        else:
            return False

    #Adds letter to the text
    def AddLetter(self, letter):
        self.text += letter 

    #Removes a letter if the text is not nothing, removes a word if control is true    
    def RemoveLetter(self, control):
        if self.text != "":
            if control:
                if self.__hashedOut:
                    self.text = ""
                else:
                    #Removes trailing spaces 
                    while self.text[-1] == " ":
                        self.text = self.text[:-1]
                    #Removes letters until a space is reached or text has run out
                    while self.text != "" and self.text[-1] != " ":
                        self.text = self.text[:-1]
            else:
                self.text = self.text[:-1]

    #Sets colour to match the selection status of the box
    def SetActive(self):
        self.__colour = self.__colourActive
        self.isActive = True

    #Sets colour to match the selection status of the box
    def SetDormant(self):
        self.__colour = self.__colourDormant
        self.isActive = False

#--------------------------------
#This stuff can be ignored, was used for testing and is only still here in case I need it later.
#--------------------------------

# dispWidth = 1920
# dispHeight = 1080
# window = pygame.display.set_mode((dispWidth, dispHeight))
# pygame.display.set_caption("SpeedTyper")
# pygame.font.init()

# #Boxlocations
# userBoxWidth = 600 * dispWidth / 1920
# rectangleUsernameBox = pygame.rect.Rect((0,int(400 * dispHeight/1080)), (int(1000 * dispWidth / 1920), int(70 * dispHeight / 1080)))
# rectangleUsernameBox.centerx = dispWidth / 2
# usernameBox = InputBox((255,255,255), (35,35,35), (30,30,30), False, rectangleUsernameBox, dispHeight)

# rectanglePasswordBox = pygame.rect.Rect((0,int(400 * dispHeight/1080)), (int(1000 * dispWidth / 1920), int(70 * dispHeight / 1080)))
# rectanglePasswordBox.centerx = dispWidth / 2
# rectanglePasswordBox.centery += int((80 + rectanglePasswordBox.height / 2 + rectangleUsernameBox.height / 2) * dispHeight / 1080)
# passwordBox = InputBox((255,255,255), (35,35,35), (30,30,30), True, rectanglePasswordBox, dispHeight)


# running = True

# backspace = False
# timeSinceLastBackspace = 0
# timeBetweenBackspaces = 50
# usernameBoxSelected = False
# passWordBoxSelected = False
# control = False
# clock = pygame.time.Clock()

# while running:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         clickLocation = pygame.mouse.get_pos()
    #         if usernameBox.CheckIfClicked(clickLocation):
    #             usernameBox.SetActive()
    #             usernameBoxSelected = True

    #         else:
    #             usernameBox.SetDormant()
    #             usernameBoxSelected = False

    #         if passwordBox.CheckIfClicked(clickLocation):
    #             passwordBox.SetActive()
    #             passWordBoxSelected = True

    #         else:
    #             passwordBox.SetDormant()
    #             passWordBoxSelected = False

    #     elif event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_BACKSPACE:
    #             backspace = True
                
    #             if usernameBoxSelected:
    #                 usernameBox.RemoveLetter(control)
    #             elif passWordBoxSelected:
    #                 passwordBox.RemoveLetter(control)

    #             timeSinceLastBackspace = -200

    #         elif event.key == pygame.K_RETURN:
    #             pass

    #         elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
    #             control = True

    #         else:
    #             if usernameBoxSelected:
    #                 usernameBox.AddLetter(event.unicode)
    #             elif passWordBoxSelected:
    #                 passwordBox.AddLetter(event.unicode)

    #     elif event.type == pygame.KEYUP:
    #         if event.key == pygame.K_BACKSPACE:
    #             backspace = False

    #         elif event.key == pygame.K_RETURN:
    #             pass

    #         elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
    #             control = False

    # if backspace and timeSinceLastBackspace > timeBetweenBackspaces:
    #     if usernameBoxSelected:
    #         usernameBox.RemoveLetter(control)
    #     elif passWordBoxSelected:
    #         passwordBox.RemoveLetter(control)

    #     timeSinceLastBackspace = 0

    # clock.tick()
    # timeSinceLastBackspace += clock.get_time()

#     window.fill((10,10,10))
#     usernameBox.DrawBox(window)
#     passwordBox.DrawBox(window)
#     pygame.display.update()