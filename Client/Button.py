import pygame

#This object is a button that can be clicked to do certain actions 
class Button:
    #Location is the top left coordinates
    #Size is (width, height) tuple
    def __init__(self, text, location, size, backColourDormant, backColourActive, textColour, dispHeight):
        self.__pressed = False
        self.__text = text
        self.__location = location
        self.__size = size
        self.rectangle = pygame.Rect(self.__location, self.__size)
        self.__backColourDormant = backColourDormant
        self.__backColourActive = backColourActive
        self.__backColour = self.__backColourDormant
        self.__textColour = textColour

        #Finds correct fontsize
        fontSize = 1
        font = pygame.font.SysFont("Courier New", int(fontSize))
        fontRenderSize = font.size(self.__text)
        #Checks if the text will fit in the texbox
        while fontRenderSize[0] < self.__size[0] and fontRenderSize[1] < self.__size[1]:
            fontSize += 1
            font = pygame.font.SysFont("Courier New", int(fontSize))
            fontRenderSize = font.size(self.__text)

        self.__font = pygame.font.SysFont("Courier New", int(fontSize - 1))

    def SetFont(self, font):
        self.__font = font

    #Sets center to the new position
    def SetLocation(self, pos):
        self.rectangle.center = pos
        self.__location = (self.rectangle.x, self.rectangle.y)

    def SetText(self, text):
        self.__text = text

    def GetText(self):
        return self.__text

    def Render(self, window):
        pygame.draw.rect(window, self.__backColour, self.rectangle)
        textRenderSize = self.__font.size(self.__text)

        #location of text = top right of box + half of the difference of width, top right of box + half of the difference of height (between the box and text)
        textRenderLocation = (self.__location[0] + (self.__size[0] - textRenderSize[0]) / 2, self.__location[1] + (self.__size[1] - textRenderSize[1]) / 2)

        textRender = self.__font.render(self.__text, True, self.__textColour)
        window.blit(textRender, textRenderLocation)

    def SetActive(self):
        self.__backColour = self.__backColourActive
        
    def SetDormant(self):
        self.__backColour = self.__backColourDormant

    def CheckIfHovering(self, mousePos):
        if self.rectangle.collidepoint(mousePos):
            return True

        else:
            return False

    def GetPressedState(self):
        return self.__pressed

    def Pressed(self):
        self.__pressed = True

    def DePressed(self):
        self.__pressed = False

#These are commented out as I might need them later
# import ctypes

# user32 = ctypes.windll.user32
# #Prevents the screen from scaling with windows resolution scale
# user32.SetProcessDPIAware()
# #Gets the screen resolution
# dispWidth = user32.GetSystemMetrics(0)
# dispHeight = user32.GetSystemMetrics(1)

# window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# pygame.display.set_caption("SpeedTyper")
# pygame.font.init()

# ThisButton = Button("TestButton", (dispWidth / 2, dispHeight / 2), (500,500), (30,30,30), (100,100,100), (255,255,255), 1080)

# running = True
# stillInBox = False
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             if ThisButton.CheckIfHovering(pygame.mouse.get_pos()):
#                 stillInBox = True
#                 print("Clicked on box")

#         elif event.type == pygame.MOUSEBUTTONUP and stillInBox:
#             ThisButton.Pressed()

#     if ThisButton.CheckIfHovering(pygame.mouse.get_pos()):
#         ThisButton.SetActive()
    
#     else:
#         ThisButton.SetDormant()
#         stillInBox = False

#     ThisButton.Render(window)
#     pygame.display.update()