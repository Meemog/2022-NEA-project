import pygame
from TextBox import TextBox
from InputHandler import InputHandler
from Renderer import Renderer
from wordGeneration import wordGenerator

class Game:
    def __init__(self, dispWidth, dispHeight):
        self.__gameClock = pygame.time.Clock() #makes a clock object
        self.__inputHandler = InputHandler()
        self.__timeBetweenBacspaces = 50
        self.__timeSinceLastBackspace = 0
        self.__deleting = False
        self.__renderer = Renderer()
        wordGen = wordGenerator()
        self.__backText = wordGen.GetWordsForProgram(500)
        self.__textBox = TextBox(int(dispWidth - (dispWidth * 2/5)), int(50 * dispHeight / 1080), (int(dispWidth / 5), int(6 * dispHeight / 20)), (40,40,40), (30,30,30), (255,144,8), int(dispHeight*42/1080), self.__backText, (20,20,20))

    def main(self, window):
        GAMELOOP = True
        while GAMELOOP:
            self.__gameClock.tick()
            pygame.time.delay(30)   #determines max fps of game
            commands = self.__inputHandler.HandleInput(self.__textBox.box)
            for command in commands:
                print(command)
                if command == "QUIT":
                    GAMELOOP = False

                elif command[0] == "K":
                    command = command[1:]
                    self.__textBox.AddLetter(command)

                elif command == "CLICKED ON BOX":
                    self.__textBox.SetActive()

                elif command == "CLICKED OUT OF BOX":
                    self.__textBox.SetDormant()

                elif command == "BACKSPACE DOWN":
                    self.__textBox.DeleteLetter()
                    self.__deleting = True
                    self.__timeSinceLastBackspace = -200

                elif command == "BACKSPACE UP":
                    self.__deleting = False

            #Deletes text while backspace being held down
            if self.__deleting and self.__timeSinceLastBackspace > self.__timeBetweenBacspaces and self.__inputHandler.typing:
                self.__textBox.DeleteLetter()
                self.__timeSinceLastBackspace = 0
            
            #Adds time since last frame to time since last backspace
            self.__timeSinceLastBackspace += self.__gameClock.get_time()

            #Draws everything
            self.__renderer.Render(window, self.__textBox)

        return 0
