import pygame
import random
pygame.init()

window = pygame.display.set_mode((500,500))
pygame.display.set_caption("Test window")

playerHeight = 50
playerWidth = 50
playerX = 100
playerY = 300
playerVelocity = 5

red = 0
green = 0
blue = 0
colourSpeed = 5

run = True
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if red < 255 and colourSpeed > 0:
        red += colourSpeed

    elif red >= 255:
        if green < 255 and colourSpeed > 0:
            blue += colourSpeed

        elif green >= 255:
            if blue < 255 and colourSpeed > 0:
                blue += colourSpeed
            
            elif blue >= 255:
                colourSpeed *= -1            

    pygame.draw.rect(window, (red, green, blue), (playerX, playerY, playerWidth, playerHeight))
    pygame.display.update()

pygame.quit()