import pygame

class Renderer:
    def __init__(self, dispHeight):
        self.__backColour = (10,10,10)
        self.__font = pygame.font.SysFont("Courier New", int(dispHeight * 60/1080))
    
    #Used in part where client is waiting for the game to start
    #Renders a number
    def RenderTimer(self, window, screenDimensions, seconds):
        numRender = self.__font.render(str(seconds), True, (255,255,255))
        renderSize = self.__font.size(str(seconds))
        window.blit(numRender, ((screenDimensions[0] - renderSize[0]) / 2, (screenDimensions[1] - renderSize[1]) / 2))
        pygame.display.update()

    def Render(self, window, textBox):
        window.fill(self.__backColour)
        pygame.draw.rect(window, textBox.boxColour, textBox.box)
        textBox.DrawBox(window)

        pygame.display.update()