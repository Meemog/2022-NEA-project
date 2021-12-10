import pygame

class Renderer:
    def __init__(self):
        self.__backColour = (10,10,10)
    
    #Draws everything on screen
    def Render(self, window, textBox):
        window.fill(self.__backColour)
        pygame.draw.rect(window, textBox.boxColour, textBox.box)
        textBox.DrawBox(window)

        pygame.display.update()