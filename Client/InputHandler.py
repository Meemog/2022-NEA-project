import pygame
from DataStructures import PriorityQueue
#Object that stores list of inputs made by user
class InputHandler:
    def __init__(self):
        #Priority queue for storing userinputs
        self.inputsPriorityQueue = PriorityQueue()

    #Checks for inputs and adds them to the priority queue
    def CheckInputs(self):
        #For event in events that happened
        for event in pygame.event.get():
            #If the player quit
            if event.type == pygame.QUIT:
                #High priority = front of queue
                self.inputsPriorityQueue.Enqueue(999, "QUIT")
            
            #If player clicks, appends the mouse location to the command that player clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                command = f"CLICK:{mousePos[0]},{mousePos[1]}"
                self.inputsPriorityQueue.Enqueue(0, command)
            
            #If player stops clicking, same as clicking
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                command = f"UNCLICK:{mousePos[0]},{mousePos[1]}"
                self.inputsPriorityQueue.Enqueue(0, command)

            #Handling keyboard inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.inputsPriorityQueue.Enqueue(0, "RETURNDOWN")

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.inputsPriorityQueue.Enqueue(0, "SHIFTDOWN")

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.inputsPriorityQueue.Enqueue(0, "CONTROLDOWN")

                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.inputsPriorityQueue.Enqueue(0, "ALTDOWN")
                
                elif event.key == pygame.K_BACKSPACE:
                    self.inputsPriorityQueue.Enqueue(0, "BACKSPACEDOWN")

                elif event.key == pygame.K_TAB:
                    self.inputsPriorityQueue.Enqueue(0, "TABDOWN")

                else:
                    #KD = KeyDown
                    self.inputsPriorityQueue.Enqueue(0, f"KD_{event.unicode}")
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.inputsPriorityQueue.Enqueue(0, "RETURNUP")

                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self.inputsPriorityQueue.Enqueue(0, "SHIFTUP")

                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self.inputsPriorityQueue.Enqueue(0, "CONTROLUP")

                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    self.inputsPriorityQueue.Enqueue(0, "ALTUP")

                elif event.key == pygame.K_BACKSPACE:
                    self.inputsPriorityQueue.Enqueue(0, "BACKSPACEUP")

                elif event.key == pygame.K_TAB:
                    self.inputsPriorityQueue.Enqueue(0, "TABUP")

                else:
                    #KU = KeyUp
                    self.inputsPriorityQueue.Enqueue(0, f"KU_{event.unicode}")

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
#     input = inputHandler.inputsPriorityQueue.Dequeue()
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

#         input = inputHandler.inputsPriorityQueue.Dequeue()

#     #Returns unused inputs back into priority list
#     for input in ignoredInputs:
#         inputHandler.inputsPriorityQueue.Enqueue(input[0], input[1])

# print(text)