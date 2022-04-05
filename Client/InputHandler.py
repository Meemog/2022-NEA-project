import pygame

#Object that stores list of inputs made by user
class InputHandler:
    def __init__(self):
        #Priority queue for storing userinputs
        self.inputsList = []

    #Checks for inputs and adds them to the priority queue
    def CheckInputs(self):
        #For event in events that happened
        for event in pygame.event.get():
            #If the player quit
            if event.type == pygame.QUIT:
                #High priority = front of queue
                self.inputsList.append("QUIT")
            
            #If player clicks, appends the mouse location to the command that player clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                command = f"CLICK:{mousePos[0]},{mousePos[1]}"
                self.inputsList.append(command)
            
            #If player stops clicking, same as clicking
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                command = f"UNCLICK:{mousePos[0]},{mousePos[1]}"
                self.inputsList.append(command)

            #Handling keyboard inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.inputsList.append("RETURNDOWN")

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.inputsList.append("SHIFTDOWN")

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.inputsList.append("CONTROLDOWN")

                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.inputsList.append("ALTDOWN")
                
                elif event.key == pygame.K_BACKSPACE:
                    self.inputsList.append("BACKSPACEDOWN")

                elif event.key == pygame.K_TAB:
                    self.inputsList.append("TABDOWN")

                else:
                    #KD = KeyDown
                    self.inputsList.append(f"KD_{event.unicode}")
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.inputsList.append("RETURNUP")

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.inputsList.append("SHIFTUP")

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.inputsList.append("CONTROLUP")

                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.inputsList.append("ALTUP")

                elif event.key == pygame.K_BACKSPACE:
                    self.inputsList.append("BACKSPACEUP")

                elif event.key == pygame.K_TAB:
                    self.inputsList.append("TABUP")

                else:
                    #KU = KeyUp
                    self.inputsList.append(f"KU_{event.unicode}")
