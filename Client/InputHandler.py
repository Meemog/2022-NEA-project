import pygame

class InputHandler:
    def __init__(self):
        self.typing = False

    #Gets input, converts it to commands and returns a list of commands
    def HandleInput(self, box):
        commands = []
        clicked = False
        for event in pygame.event.get():
            #Alt + f4 
            if event.type == pygame.QUIT:
                commands.append("QUIT")

            #On click changes if textbox is selected or not
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(pygame.mouse.get_pos()):
                    self.typing = True
                    clicked = True
                    
                else:
                    self.typing = False
                    clicked = True

            #Checks keypresses
            elif event.type == pygame.KEYDOWN and self.typing:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE DOWN")

                elif event.key == pygame.K_RETURN:
                    pass

                elif event.key == pygame.K_LCTRL:
                    commands.append("CONTROL DOWN")

                #Adds letter pressed down as a commands 
                else:
                    commands.append(f"K{event.unicode}") 
        
            #Detects key being depressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE UP")
                
                elif event.key == pygame.K_LCTRL:
                    commands.append("CONTROL UP")

        #Determines if box should be selected or not
        if self.typing and clicked:
            commands.append("CLICKED ON BOX")

        elif not self.typing and clicked:
            commands.append("CLICKED OUT OF BOX")
        return commands

