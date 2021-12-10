#main file
import pygame
from Client import Client

dispWidth = 1920
dispHeight = 1080
window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

game = Client(dispWidth, dispHeight)
game.main(window)

pygame.font.quit()
pygame.quit()