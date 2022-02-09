from cmath import rect
import pygame

class InputBox:
    def __init__(self, textColour, colourActive, colourDormant, hashedOut, rectangle, dispHeight):
        self.text = ""
        self.__textColour = textColour
        self.__colour = colourDormant
        self.isActive = False
        self.__colourActive = colourActive
        self.__colourDormant = colourDormant
        self.__hashedOut = hashedOut
        self.__size = rectangle.size
        self.__location = (rectangle.x, rectangle.y)
        self.rectangle = rectangle

        fontSize = 999
        font = pygame.font.SysFont("Courier New", int(dispHeight * fontSize/1080))
        fontRenderSize = font.size(self.text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[1] > self.__size[1]:
            fontSize -= 1
            font = pygame.font.SysFont("Courier New", int(dispHeight * fontSize/1080))
            fontRenderSize = font.size(self.text)

        self.__font = font

    def DrawBox(self, window):
        pygame.draw.rect(window, self.__colour, self.rectangle)

        if self.__hashedOut:
            text = "*"*len(self.text)

        else:
            text = self.text

        lettersFromBack = len(text)
        #While the rendered version of text with lettersFromBack number of letters from the back is bigger than the textbox
        while self.__font.size(text[-lettersFromBack:])[0] > self.__size[0] - 10:
            lettersFromBack -= 1

        textRender = self.__font.render(text[-lettersFromBack:], True, self.__textColour)
        window.blit(textRender, (self.__location[0] + 5, self.__location[1] + 5))
        
    def CheckIfClicked(self, location):
        if self.rectangle.collidepoint(location):
            return True

        else:
            return False

    def AddLetter(self, letter):
        self.text += letter 

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

    def SetActive(self):
        self.__colour = self.__colourActive
        self.isActive = True

    def SetDormant(self):
        self.__colour = self.__colourDormant
        self.isActive = False

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