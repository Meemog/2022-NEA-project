#main file
import pygame
from Game import Game

dispWidth = 1920    #Sets resolution
dispHeight = 1080
window = pygame.display.set_mode((dispWidth, dispHeight))   #Creates window object
pygame.display.set_caption("SpeedTyper")                    #Captions window object
pygame.font.init()                                          #Initialises the font module in pygame

game = Game(dispWidth, dispHeight)                          #Creates game object where game is ran
game.main(window)                                           #Runs the main() method from the game object

pygame.font.quit()                                          #Closes font module from pygame // Not sure if this matters, but docs said to use it
pygame.quit()                                               #Closes the game