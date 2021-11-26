import pygame

#Converts input from event objects to commands recognised by rest of program
class InputHandler:
    def __init__(self):
        self.typing = False

    def HandleInput(self, box):
        commands = []       #Command list that is added to
        clicked = False     #Prevents the need to add multiple commands that would need to be processed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                commands.append("QUIT")

            #Checks if mouse is on box when click happened
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(pygame.mouse.get_pos()):
                    self.typing = True
                    clicked = True
                    
                else:
                    self.typing = False
                    clicked = True

            #Checks for keys being pressed
            elif event.type == pygame.KEYDOWN and self.typing:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE DOWN")

                elif event.key == pygame.K_RETURN:
                    pass

                elif event.key == pygame.K_LCTRL:
                    commands.append("CONTROL DOWN")

                else:
                    commands.append(f"K{event.unicode}")        #Appends whatever wasn't detected
        
            #Detects keys being depressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE UP")
                
                elif event.key == pygame.K_LCTRL:
                    commands.append("CONTROL UP")

        #Determines if box is active or not (in case of multiple clicks in a single frame)
        if self.typing and clicked:
            commands.append("CLICKED ON BOX")

        elif not self.typing and clicked:
            commands.append("CLICKED OUT OF BOX")

        return commands    #Returns a list of strings