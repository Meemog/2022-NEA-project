#main file
import pygame
import ctypes
from Game import Game

user32 = ctypes.windll.user32
#Prevents the screen from scaling with windows resolution scale
#System -> Display -> Scale and Layout
user32.SetProcessDPIAware()
# Alternative way of getting screen resolution
# dispWidth = user32.GetSystemMetrics(0)
# dispHeight = user32.GetSystemMetrics(1)

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
