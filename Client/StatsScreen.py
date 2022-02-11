import pygame
from Button import Button

class StatsScreen:
    def __init__(self, screenDim):
        #TODO the text at the top
        #Text at the top
        textFont = pygame.font.SysFont("Calibri", 72 * screenDim[1] / 1080)
        self.__textRender = textFont.render("Player statistics", True, (160,160,160))
        self.__textPos = (190 * screenDim[0] / 1920, 130 * screenDim[1] / 1080)

        #TODO the grey background
        #Grey backgrond
        
        #TODO the stats text itself

        #TODO the return button
