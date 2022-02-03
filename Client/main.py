#main file
import pygame
from Game import Game
# import atexit

dispWidth = 500
dispHeight = 500
window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

# #Detects if the program is closed
# def QuitGame():
#     game.userQuit = True

# atexit.register(QuitGame)

game = Game(dispWidth, dispHeight)
game.main(window)

pygame.font.quit()
pygame.quit()
