#main file
import pygame
from Client import Client

dispWidth = 500
dispHeight = 500
window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

game = Client()
game.main(window, dispWidth, dispHeight)

pygame.font.quit()
pygame.quit()