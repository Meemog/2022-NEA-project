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
            elif event.type == pygame.MOUSEBUTTONDOWN:
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

# import ctypes
# from Game import Game

# user32 = ctypes.windll.user32
# user32.SetProcessDPIAware()

# window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# pygame.display.set_caption("SpeedTyper")
# pygame.font.init()

# inputHandler = InputHandler()

# text = ""
# playerQuit = False
# while not playerQuit:
#     inputHandler.CheckInputs()
#     input = inputHandler.inputsList.Dequeue()
#     ignoredInputs = []
#     #Goes through every input
#     while input != []:
#         # print(f"Priority: {input[0]}\nInput: {input[1]}\n")
#         if input[1] == "QUIT":
#             playerQuit = True
#         elif input[1][:3] == "KD_":
#             text += input[1][3:]
#         elif input[1][:6] == "CLICK:":
#             clickLocation = input[1][6:].split(",")
#             print(f"Clicked at ({clickLocation[0]},{clickLocation[1]})")
#         else:
#             ignoredInputs.append(input)

#         input = inputHandler.inputsList.Dequeue()

#     #Returns unused inputs back into priority list
#     for input in ignoredInputs:
#         inputHandler.inputsList.append(input[0], input[1])

# print(text)