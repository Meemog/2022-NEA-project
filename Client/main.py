#main file
import pygame
import ctypes
from Game import Game

#Sets to ignore windows scale setting
#System -> Display -> Scale and Layout
ctypes.windll.user32.SetProcessDPIAware()

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

res = pygame.display.Info()
dispWidth = res.current_w
dispHeight = res.current_h

game = Game(dispWidth, dispHeight)
game.main(window)

pygame.font.quit()
pygame.quit()
