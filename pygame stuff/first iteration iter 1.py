import pygame
pygame.init()

dispWidth = 500
dispHeight = 500
#sets the screen size

window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("Typeracer")
#makes a new window and captions it typeracer

boxWidth = int(dispWidth - (dispWidth * 2/5))
boxHeight = 50
#defines the box size
boxX = dispWidth / 5
boxY = dispHeight / 5
#defines the box position
boxCoords = (boxX, boxY)
boxColour = (150,150,150)
#defines box colour
box = pygame.Rect(boxCoords, (boxWidth, boxHeight))
#defines box in format of a pygame.rect()

#experimental bits
pygame.key.start_text_input()
pygame.key.set_text_input_rect(box)
#experimental bits end

GAMELOOP = True
while GAMELOOP:
    pygame.time.delay(30)
    #determines fps of the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAMELOOP = False
            #sets gameloop to false if the player presses alt + f4 or the x in the top right 

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if box.collidepoint(pygame.mouse.get_pos()):
                #checks if mouse is on the box at time of click
                boxColour = (255,255,255)
                typing = True

            else:
                typing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                boxColour = (255,0,0)

    pygame.draw.rect(window, boxColour, box)
    #draws a rectangle with colour boxColour

    pygame.display.update()
    #draws the new frame
pygame.quit()