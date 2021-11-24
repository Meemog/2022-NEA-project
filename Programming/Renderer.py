import pygame

#Renders everything 
class Renderer:
    def __init__(self):
        self.__backColour = (10,10,10)  #Determines background colour
    
    def Render(self, window, textBox):
        window.fill(self.__backColour)  #Colours background
        pygame.draw.rect(window, textBox.boxColour, textBox.box)    #Draws textbox rectangle
        textBox.DrawBox(window) #Draws rest of box such as text and preview text

        pygame.display.update() #Updates the screen
