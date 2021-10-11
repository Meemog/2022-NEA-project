import pygame
pygame.init()

dispWidth = 1920
dispHeight = 1080

#sets the screen size

window = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption("Typeracer")
#makes a new window and captions it typeracer

#makes a clock object
gameClock = pygame.time.Clock()

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
text = ''
#sets text string to empty so it can be added to later
font = pygame.font.Font(None, 32)
#sets the font to the default with size 32
textColour = (204, 186, 198)
#time between backspaces
timeBetweenBackspaces = 50
#time since last backspace
timeSinceLastBackspace = 0
#boolean for whether or not the current text is being deleted
deleting = False

#experimental bits
pygame.key.start_text_input()
pygame.key.set_text_input_rect(box)
#experimental bits end

GAMELOOP = True
while GAMELOOP:
    gameClock.tick()
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
                boxColour = (150,150,150)
                typing = False

        #handles keypress events
        elif event.type == pygame.KEYDOWN and typing:
            if event.key == pygame.K_RETURN:
                print(text) #does stuff with the text that was written
                text = ''   #resets the text to empty string
            #detects backspace being pressed down
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1] #removes 1 letter from the end of the text
                deleting = True  #enables deleting through holding down the key
                timeSinceLastBackspace = 0
            else:
                text += event.unicode
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                deleting = False
    #deletes text while the key is held down        
    if deleting and timeSinceLastBackspace > timeBetweenBackspaces and typing:                    
        text = text[:-1]
        timeSinceLastBackspace = 0

    timeSinceLastBackspace += gameClock.get_time()

    window.fill((0,0,0))
    textRender = font.render(text, True, textColour)
    pygame.draw.rect(window, boxColour, box)
    #draws a rectangle with colour boxColour
    window.blit(textRender, (boxX+5, boxY+5))

    pygame.display.update()
    #draws the new frame
pygame.quit()