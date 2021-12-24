#main file
import pygame
from Game import Game

dispWidth = 500
dispHeight = 500
window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

game = Game()
game.main(window, dispWidth, dispHeight)

pygame.font.quit()
pygame.quit()