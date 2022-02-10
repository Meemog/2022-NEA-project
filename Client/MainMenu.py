import pygame
from Button import Button

class MainMenu:
    def __init__(self, screenDimensions):
        self.__font = pygame.font.SysFont("Calibri", int(96 * screenDimensions[1] / 1080))
        self.__textRenderSize = self.__font.size("SpeedTyper")
        self.__screenDimensions = screenDimensions
        textColour = (160,160,160)

        titleColour = (255,144,8)
        self.__textRender = self.__font.render("SpeedTyper", True, titleColour)

        #For the buttons
        boxColourActive = (35,35,35)
        boxColourDormant = (30,30,30)
        buttonSize = (680 * screenDimensions[0] / 1920, 150 * screenDimensions[1] / 1080)
        self.__buttons = []

        screenCenter = screenDimensions[0] / 2 - buttonSize[0] / 2
        self.__buttons.append(Button("Play", (screenCenter, 250 * screenDimensions[1] / 1080), buttonSize, boxColourDormant, boxColourActive, textColour, screenDimensions[1]))
        self.__buttons.append(Button("Statistics", (screenCenter, 450 * screenDimensions[1] / 1080), buttonSize, boxColourDormant, boxColourActive, textColour, screenDimensions[1]))
        self.__buttons.append(Button("Settings", (screenCenter, 650 * screenDimensions[1] / 1080), buttonSize, boxColourDormant, boxColourActive, textColour, screenDimensions[1]))
        self.__buttons.append(Button("Quit", (screenCenter, 850 * screenDimensions[1] / 1080), buttonSize, boxColourDormant, boxColourActive, textColour, screenDimensions[1]))

        #Overrides all buttons' fonts to have same size
        for button in self.__buttons:
            button.SetFont(self.__font)

    def Render(self, window):
        window.blit(self.__textRender, (self.__screenDimensions[0] / 2 - self.__textRenderSize[0] / 2, 110 * self.__screenDimensions[1] / 1080))
        for button in self.__buttons:
            button.Render(window)

    def Run(self, window, settings):
        running = True
        playerQuit = False
        while running:
            mousePos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    playerQuit = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.__buttons:
                        if button.CheckIfHovering(mousePos):
                            button.Pressed()

            for button in self.__buttons:
                if button.CheckIfHovering(mousePos):
                    button.SetActive()
                else:
                    button.SetDormant()

                if button.GetPressedState():
                    if button.GetText() == "Play":
                        running = False
                        pass

                    elif button.GetText() == "Statistics":
                        #Go to statistics
                        pass

                    elif button.GetText() == "Settings":
                        #Go to settings
                        pass

                    elif button.GetText() == "Quit":
                        running = False
                        playerQuit = True

            #Rendering 
            window.fill((10,10,10))
            self.Render(window)
            pygame.display.update()

        if playerQuit:
            return False

        else:
            return True

# dispWidth = 500    
# dispHeight = 500
# window = pygame.display.set_mode((dispWidth, dispHeight))
# pygame.display.set_caption("SpeedTyper")
# pygame.font.init()

# menu = MainMenu((dispWidth, dispHeight))
# menu.Run()

# pygame.font.quit()
# pygame.quit()